---
layout: post
title: From NanoGPT Internals to a ChatGPT-Style Chatbot
date: 2025-02-12 11:59:00-0400
categories: LLM
gisqus_comments: true
---

In this post, I share a concise overview of how NanoGPT works and how I extended it into building a ChatGPT-style chatbot. We'll cover the key building blocks—Attention Mechanisms, Positional Embeddings, and the Training Loop—and then discuss the steps needed for fine-tuning a model into a chatbot using RLHF techniques.

---

## **Table of Contents**

1. [Why NanoGPT?](#why-nanogpt)  
2. [Attention Mechanisms](#attention-mechanisms)  
3. [Positional Embeddings](#positional-embeddings)  
4. [Core Training Loop](#core-training-loop)  
5. [Building a ChatGPT-Style Bot](#building-a-chatgpt-style-bot)  
   - [Pretraining / Starting from a Base Model](#pretraining--starting-from-a-base-model)  
   - [Supervised Fine-Tuning (SFT)](#supervised-fine-tuning-sft)  
   - [Reward Model Training](#reward-model-training)  
   - [RLHF (PPO)](#rlhf-ppo)  
6. [Conclusion](#conclusion)

---

## **Why NanoGPT?**

[NanoGPT](https://github.com/karpathy/nanoGPT) is a simple implementation of a causal, decoder-only Transformer built by [Andrej Karpathy](https://twitter.com/karpathy). It provided a minimalist approach to learning how GPT-style models work. The implementation of a causal, decoder-only Transformer helped me focus on the fundamentals without getting lost in excessive complexity. There is also a [video tutorial series](https://karpathy.ai/zero-to-hero.html) by Andrej Karpathy on building LLMs from scratch which I highly recommend.

Key advantages:
- **Self-Attention Made Simple**: A clear view into how tokens interact.
- **Straightforward Positional Embeddings**: Easily grasp the concept of token order.
- **Basic Training Loop**: Understand next-token prediction with cross-entropy loss.

---

## **Attention Mechanisms**

### **Overview**

The self-attention mechanism allows the model to weigh each token relative to every other token in a sequence. This is done by computing Query, Key, and Value vectors and then using their interactions to form attention scores.

Below is a simplified version of a self-attention layer:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        
        # Linear layers for Q, K, V
        self.query = nn.Linear(embed_dim, embed_dim)
        self.key = nn.Linear(embed_dim, embed_dim)
        self.value = nn.Linear(embed_dim, embed_dim)
        
        # Final projection
        self.proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        B, T, C = x.shape
        q = self.query(x)
        k = self.key(x)
        v = self.value(x)
        
        # Reshape and compute attention scores
        q = q.view(B, T, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        k = k.view(B, T, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        v = v.view(B, T, self.num_heads, self.head_dim).permute(0, 2, 1, 3)
        att_scores = (q @ k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        
        mask = torch.triu(torch.ones(T, T, device=x.device), diagonal=1).bool()
        att_scores = att_scores.masked_fill(mask, float('-inf'))
        
        att_weights = F.softmax(att_scores, dim=-1)
        out = att_weights @ v
        
        out = out.permute(0, 2, 1, 3).contiguous().view(B, T, C)
        return self.proj(out)
```

---

## **Positional Embeddings**

### **Overview**

Since Transformers don't inherently process token order, positional embeddings provide each token with information about its position in the sequence. This fixed method—using sine and cosine functions—adds no extra parameters.

```python
class PositionalEncoding(nn.Module):
    def __init__(self, embed_dim, max_length=1024):
        super().__init__()
        pe = torch.zeros(max_length, embed_dim)
        position = torch.arange(0, max_length, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-torch.log(torch.tensor(10000.0)) / embed_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        seq_len = x.size(1)
        return x + self.pe[:, :seq_len, :]
```

---

## **Core Training Loop**

The training loop for NanoGPT involves predicting the next token. Here is a condensed version:

```python
import torch
import torch.nn as nn
import torch.optim as optim

model = GPTModel(...)  # Your GPT-like model
optimizer = optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for step in range(max_steps):
    x, y = get_batch('train')
    logits = model(x)  # (batch_size, seq_len, vocab_size)
    loss = loss_fn(logits.view(-1, logits.size(-1)), y.view(-1))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if step % 100 == 0:
        print(f"Step {step}, train loss: {loss.item():.4f}")
```

This loop emphasizes simplicity while laying the foundation for more complex training strategies.

---

## **Building a ChatGPT-Style Bot**

Since NanoGPT has already been trained as a base language model, the next step is aligning it for conversational tasks. This involves two key stages: **Reward Model Training** and **RLHF (PPO)**.

### Reward Model Training

To evaluate and rank generated responses, you can train a reward model. The reward model takes latent representations from the base GPT model and outputs a scalar reward that reflects response quality. Below is a simplified example using PyTorch:

```python
import torch
import torch.nn as nn

class RewardModel(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.linear = nn.Linear(hidden_dim, 1)
    
    def forward(self, hidden_states):
        # hidden_states: (batch, seq_len, hidden_dim)
        # Using mean pooling over the sequence for a simple summary
        pooled = hidden_states.mean(dim=1)  
        reward = self.linear(pooled).squeeze(-1)  
        return reward

# Example usage:
hidden_dim = 768  # Example hidden dimension
reward_model = RewardModel(hidden_dim)

# Simulate some hidden representations (for example from a GPT model)
dummy_hidden = torch.randn(2, 50, hidden_dim)  # (batch, seq_len, hidden_dim)
reward_scores = reward_model(dummy_hidden)
print("Reward scores:", reward_scores)
```

This reward model can later be trained on human preference data to accurately score responses.

### RLHF (PPO) for Fine-Tuning

With a trained reward model, you can further fine-tune your GPT model using reinforcement learning. One common approach is to use Proximal Policy Optimization (PPO) to adjust the model based on the reward signals. The TRL (Transformer Reinforcement Learning) library by HuggingFace simplifies these steps. Below is an example:

```python
from trl import PPOTrainer, PPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load a GPT-like model and its tokenizer (using GPT-2 here for demonstration)
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Setup PPO configuration
ppo_config = PPOConfig(
    learning_rate=1e-5,
    batch_size=2,
    ppo_epochs=4,
    init_kl_coef=0.1,
    target=6.0,
)

# Initialize the PPO trainer
ppo_trainer = PPOTrainer(
    config=ppo_config,
    model=model,
    ref_model=model,  # using the same model as a reference
    tokenizer=tokenizer,
)

# Sample prompt and generate a response
template = "User: How can I improve my coding skills?\nAssistant:"
inputs = tokenizer(template, return_tensors="pt")
response_ids = model.generate(**inputs, max_length=50)
response_text = tokenizer.decode(response_ids[0], skip_special_tokens=True)
print("Generated response:", response_text)

# Assume a reward score (in practice, this comes from your trained reward model)
reward = torch.tensor([1.0])  

# Perform a PPO step
ppo_stats = ppo_trainer.step(inputs["input_ids"], response_ids, reward)
print("PPO training stats:", ppo_stats)
```

These examples illustrate how to set up a reward model and integrate RLHF using PPO to further align your base model into a chatbot. This approach refines responses to be more coherent and contextually relevant without redoing the base training.

---
