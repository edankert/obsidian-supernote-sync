"""
Workflow management endpoints for Obsidian-Supernote Sync.

Provides:
- GET /workflows - List available workflows
- GET /workflows/{id} - Get workflow details
- POST /workflows - Create/update workflow
- POST /workflows/{id}/run - Execute a workflow
- DELETE /workflows/{id} - Delete a workflow
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()


# Models

class WorkflowStep(BaseModel):
    """A single step in a workflow."""

    type: str = Field(..., description="Step type (source, filter, convert, output)")
    action: str = Field(..., description="Action to perform")
    config: dict[str, Any] = Field(default_factory=dict, description="Step configuration")


class Workflow(BaseModel):
    """A complete workflow definition."""

    id: str = Field(..., description="Unique workflow identifier")
    name: str = Field(..., description="Human-readable name")
    description: str | None = Field(default=None, description="Workflow description")
    note_type: Literal["standard", "realtime"] = Field(
        default="standard",
        description="Default note type for conversions"
    )
    device: str = Field(default="A5X2", description="Target device")
    steps: list[WorkflowStep] = Field(default_factory=list, description="Workflow steps")
    created_at: str | None = None
    updated_at: str | None = None


class WorkflowRunRequest(BaseModel):
    """Request to run a workflow."""

    input_paths: list[str] | None = Field(
        default=None,
        description="Override input paths (optional)"
    )
    output_dir: str | None = Field(
        default=None,
        description="Override output directory (optional)"
    )
    dry_run: bool = Field(
        default=False,
        description="Preview what would happen without executing"
    )


class WorkflowRunResult(BaseModel):
    """Result of running a workflow."""

    workflow_id: str
    success: bool
    files_processed: int = 0
    files_succeeded: int = 0
    files_failed: int = 0
    errors: list[str] = Field(default_factory=list)
    output_files: list[str] = Field(default_factory=list)
    dry_run: bool = False


# In-memory workflow storage (will be replaced with file/DB storage)
_workflows: dict[str, Workflow] = {}


def _get_predefined_workflows_dir() -> Path:
    """Get path to predefined workflows in examples directory."""
    # Navigate from api/routes to project root
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent.parent
    return project_root / "examples" / "configs"


def _load_predefined_workflows() -> None:
    """Load predefined workflows from YAML files."""
    workflows_dir = _get_predefined_workflows_dir()
    if not workflows_dir.exists():
        logger.warning(f"Workflows directory not found: {workflows_dir}")
        return

    for yaml_file in workflows_dir.glob("*.yml"):
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or "workflow" not in data:
                continue

            workflow_data = data["workflow"]
            workflow_id = yaml_file.stem.replace("-config", "")

            # Create workflow from YAML
            workflow = Workflow(
                id=workflow_id,
                name=workflow_data.get("name", workflow_id),
                description=workflow_data.get("description"),
                note_type=workflow_data.get("note_type", "standard"),
                device=data.get("device", {}).get("model", "A5X2"),
                steps=_parse_workflow_steps(data),
            )

            _workflows[workflow_id] = workflow
            logger.info(f"Loaded predefined workflow: {workflow_id}")

        except Exception as e:
            logger.warning(f"Failed to load workflow from {yaml_file}: {e}")


def _parse_workflow_steps(data: dict) -> list[WorkflowStep]:
    """Parse workflow steps from YAML data."""
    steps = []

    # Add source step from paths config
    if "paths" in data:
        paths = data["paths"]
        if "obsidian_vault" in paths:
            source_folder = paths.get("daily_notes_folder") or paths.get(
                "research_folder"
            ) or paths.get("worldbuilding_folder", "")

            steps.append(WorkflowStep(
                type="source",
                action="folder",
                config={
                    "vault": paths.get("obsidian_vault", ""),
                    "folder": source_folder,
                    "pattern": "*.md",
                },
            ))

    # Add convert step
    workflow_data = data.get("workflow", {})
    note_type = workflow_data.get("note_type", "standard")
    steps.append(WorkflowStep(
        type="convert",
        action="md-to-note",
        config={
            "realtime": note_type == "realtime",
        },
    ))

    # Add output step
    if "paths" in data:
        paths = data["paths"]
        output_folder = paths.get("output_folder") or paths.get("supernote_folder", "")
        steps.append(WorkflowStep(
            type="output",
            action="save",
            config={
                "folder": output_folder,
            },
        ))

    return steps


# Initialize predefined workflows on module load
_load_predefined_workflows()


# Endpoints

@router.get("", response_model=list[Workflow])
async def list_workflows() -> list[Workflow]:
    """
    List all available workflows.

    Returns both predefined workflows (from examples/configs/)
    and user-created workflows.
    """
    return list(_workflows.values())


@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str) -> Workflow:
    """
    Get details of a specific workflow.
    """
    if workflow_id not in _workflows:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")
    return _workflows[workflow_id]


@router.post("", response_model=Workflow)
async def create_or_update_workflow(workflow: Workflow) -> Workflow:
    """
    Create a new workflow or update an existing one.
    """
    now = datetime.now().isoformat()

    if workflow.id in _workflows:
        workflow.updated_at = now
        workflow.created_at = _workflows[workflow.id].created_at
    else:
        workflow.created_at = now
        workflow.updated_at = now

    _workflows[workflow.id] = workflow
    logger.info(f"Saved workflow: {workflow.id}")

    return workflow


@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str) -> dict[str, str]:
    """
    Delete a workflow.
    """
    if workflow_id not in _workflows:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")

    del _workflows[workflow_id]
    logger.info(f"Deleted workflow: {workflow_id}")

    return {"status": "deleted", "workflow_id": workflow_id}


@router.post("/{workflow_id}/run", response_model=WorkflowRunResult)
async def run_workflow(workflow_id: str, request: WorkflowRunRequest) -> WorkflowRunResult:
    """
    Execute a workflow.

    Runs all steps in the workflow, converting files according
    to the workflow configuration.
    """
    if workflow_id not in _workflows:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")

    workflow = _workflows[workflow_id]

    if request.dry_run:
        return WorkflowRunResult(
            workflow_id=workflow_id,
            success=True,
            dry_run=True,
            files_processed=0,
            files_succeeded=0,
            files_failed=0,
        )

    # Execute workflow
    try:
        result = await _execute_workflow(workflow, request)
        return result
    except Exception as e:
        logger.exception(f"Workflow execution failed: {workflow_id}")
        return WorkflowRunResult(
            workflow_id=workflow_id,
            success=False,
            errors=[str(e)],
        )


async def _execute_workflow(
    workflow: Workflow,
    request: WorkflowRunRequest,
) -> WorkflowRunResult:
    """Execute a workflow and return results."""
    from obsidian_supernote.converters import convert_markdown_to_note

    errors: list[str] = []
    output_files: list[str] = []
    files_processed = 0
    files_succeeded = 0

    # Get input files
    input_paths = request.input_paths or []

    # If no explicit input paths, try to get from workflow source step
    if not input_paths:
        for step in workflow.steps:
            if step.type == "source" and step.action == "folder":
                vault = step.config.get("vault", "")
                folder = step.config.get("folder", "")
                pattern = step.config.get("pattern", "*.md")

                if vault and folder:
                    source_dir = Path(vault) / folder
                    if source_dir.exists():
                        input_paths = [str(p) for p in source_dir.glob(pattern)]
                break

    if not input_paths:
        return WorkflowRunResult(
            workflow_id=workflow.id,
            success=True,
            files_processed=0,
            files_succeeded=0,
            files_failed=0,
            errors=["No input files found"],
        )

    # Determine output directory
    output_dir = Path(request.output_dir) if request.output_dir else None
    if not output_dir:
        for step in workflow.steps:
            if step.type == "output" and step.action == "save":
                output_folder = step.config.get("folder", "")
                if output_folder:
                    output_dir = Path(output_folder)
                break

    if not output_dir:
        output_dir = Path("output")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each input file
    for input_path in input_paths:
        files_processed += 1
        p = Path(input_path)

        if not p.exists():
            errors.append(f"File not found: {input_path}")
            continue

        try:
            output_path = output_dir / f"{p.stem}.note"

            convert_markdown_to_note(
                markdown_path=p,
                output_path=output_path,
                device=workflow.device,
                realtime=(workflow.note_type == "realtime"),
            )

            output_files.append(str(output_path))
            files_succeeded += 1

        except Exception as e:
            errors.append(f"Failed to convert {input_path}: {e}")

    return WorkflowRunResult(
        workflow_id=workflow.id,
        success=(files_succeeded > 0),
        files_processed=files_processed,
        files_succeeded=files_succeeded,
        files_failed=files_processed - files_succeeded,
        errors=errors,
        output_files=output_files,
    )


@router.post("/reload")
async def reload_predefined_workflows() -> dict[str, Any]:
    """
    Reload predefined workflows from YAML files.

    This is useful if the workflow files have been edited.
    """
    global _workflows

    # Clear predefined workflows (keep user-created ones)
    predefined_ids = ["daily-notes", "research-notes", "world-building"]
    for wf_id in predefined_ids:
        if wf_id in _workflows:
            del _workflows[wf_id]

    # Reload from files
    _load_predefined_workflows()

    return {
        "status": "reloaded",
        "workflows": list(_workflows.keys()),
    }
