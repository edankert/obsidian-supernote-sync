---
title: "Attention Is All You Need - Transformer Architecture"
author: "Vaswani et al."
date: 2026-01-20
source: "https://arxiv.org/abs/1706.03762"
tags: [research, ai, transformers, deep-learning, to-supernote]
supernote.type: realtime
---

# Attention Is All You Need - Transformer Architecture

**Author:** Vaswani et al. (Google Brain)
**Source:** https://arxiv.org/abs/1706.03762
**Date Read:** 2026-01-20

## Summary

The Transformer architecture introduces a novel approach to sequence transduction
that relies entirely on self-attention mechanisms, dispensing with recurrence and
convolutions. This enables significantly more parallelization and achieves new
state-of-the-art results in machine translation.

## Key Points

1. **Self-Attention Mechanism**: Allows the model to attend to all positions in
   the input sequence simultaneously, unlike RNNs which process sequentially.

2. **Multi-Head Attention**: Uses multiple attention heads to capture different
   types of relationships between tokens.

3. **Positional Encoding**: Since there's no recurrence, positional information
   is injected via sinusoidal encodings.

4. **Encoder-Decoder Structure**: The architecture maintains the familiar
   encoder-decoder pattern but with attention-based connections.

## Annotations

<!-- Handwrite margin notes and highlights on Supernote -->
<!-- Key equations to annotate: -->
<!-- - Scaled Dot-Product Attention: Attention(Q,K,V) = softmax(QK^T/sqrt(d_k))V -->
<!-- - Multi-Head formula -->

## Questions

- How does the computational complexity compare to RNNs for very long sequences?
- What are the limitations when dealing with hierarchical structures?
- How does this relate to more recent architectures like BERT and GPT?

## Connections

- [[Neural Networks Fundamentals]]
- [[Sequence-to-Sequence Models]]
- [[BERT Architecture]]
- [[GPT Models]]

## Action Items

- [ ] Implement a simple transformer from scratch
- [ ] Compare attention visualizations across different heads
- [ ] Read follow-up paper on BERT

---

*This is a complete example of a research article ready for Supernote annotation*
