<!-- ---
layout: post
title: Finding the Guiding Tokens - Exploring LLM Predictions with Gemma-2b
date: 2024-12-26 11:59:00-0400
categories: llm embedding interpretability
gisqus_comments: true
---

# Finding the Guiding Tokens: Exploring LLM Predictions with Gemma-2b

Below is a continuation—and completion—of our deep dive into **Gemma-2b** and how we can interpret what truly guides its next-word predictions. We’ll keep it **hands-on**, **visual**, and **mathematical**, building from small and safe experiments to more **controversial** ones to illustrate the inner workings. All code snippets are *illustrative*; adapt them to your environment if you’re experimenting locally.

---

## Peeking Beneath the Hood of Gemma-2b

From our setup, recall that **Gemma-2b** is a small-scale Transformer-based LLM that can be run on modest hardware (e.g., a GPU with 4–6 GB of memory) or even CPU-bound machines if you’re patient. Despite its size, Gemma-2b follows the same fundamental architecture as larger GPT or PaLM models:

1. Text is **tokenized** into integer IDs.  
2. These tokens are mapped to **vector embeddings**.  
3. A series of **attention blocks** (multi-head self-attention + feed-forward layers) transform these embeddings.  
4. The final output is a distribution over **possible next tokens**.

### Installation (Recap)

If you haven’t installed Gemma-2b (or a similar small model) yet, you might do something like:

```bash
pip install gemma2b  # Hypothetical example
```

```python
from gemma2b import Gemma2BModel, Gemma2BTokenizer
import torch

tokenizer = Gemma2BTokenizer.from_pretrained("gemma2b")
model = Gemma2BModel.from_pretrained("gemma2b")
model.eval()  # Switch to inference mode
```

We’ll assume you already have these in place from previous parts of this tutorial.

Example 1: A Simple Completion
Let’s start with a neutral example:

```python
Copy code
input_text = "The sun rises in the"
tokens = tokenizer.encode(input_text, return_tensors="pt")

with torch.no_grad():
    output = model.generate(tokens, max_length=len(tokens[0]) + 5, num_beams=5)
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print("Input:", input_text)
print("Gemma-2b Output:", decoded_output)
```
You might see output like:

```yaml
Input: The sun rises in the
Gemma-2b Output: The sun rises in the east at dawn.
```

What’s happening internally?

Gemma-2b has learned positional, semantic, and contextual cues from training data indicating that the word “east” is strongly associated with “sun rises in the ...”.
The final layer produces a probability distribution over tokens like ("east", "morning", "sky", ...), with “east” having the highest logit.

### Visualizing the Token Embeddings
If we want to see how each token is represented in the embedding space, we could do:

```python
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

token_embeddings = model.get_input_embeddings()(tokens).squeeze(0)  # shape: [seq_len, embed_dim]

# Use PCA to reduce to 2D for visualization
pca = PCA(n_components=2)
reduced = pca.fit_transform(token_embeddings.detach().numpy())

plt.figure(figsize=(6,6))
for i, t in enumerate(tokenizer.tokenize(input_text)):
    plt.scatter(reduced[i, 0], reduced[i, 1])
    plt.text(reduced[i, 0], reduced[i, 1], t, fontsize=12)
plt.title("PCA of Token Embeddings for Sample Input")
plt.show()
```

A plot might reveal how “the”, “sun”, “rises”, etc., are spaced out in 2D. These embeddings are the first step in how Gemma-2b “understands” textual context.

Example 2: A Potentially Controversial Prompt
Let’s try:

```python
input_text = "These days wokeness has been a big "
tokens = tokenizer.encode(input_text, return_tensors="pt")

with torch.no_grad():
    output = model.generate(tokens, max_length=len(tokens[0]) + 10, num_beams=5)
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print("Input:", input_text)
print("Gemma-2b Output:", decoded_output)
```
Hypothetical output:

```yaml
Input: These days wokeness has been a big
Gemma-2b Output: These days wokeness has been a big topic of intense debate worldwide.
```

Why might it say “topic of intense debate”? Because within its training data, “wokeness” often co-occurs with words that refer to social or cultural debates. The model "knows" from patterns (frequency, attention to context, and training distribution) that “wokeness” + “has been a big” → “debate”, “topic”, or even “issue”.

### Finding the “Guiding Tokens”
One way to see which tokens in the context strongly influence the model’s next choice is to look at the attention weights in the final layers. Each attention head calculates a weighted sum of the hidden states of all previous tokens. The tokens that get the highest weights are often the “guiding tokens.”

A pseudo-code snippet:

```python
# gemma2b/model.py might have an internal structure we can poke into:
outputs = model(tokens, output_attentions=True)
# outputs.attentions is typically a tuple of shape (num_layers, num_heads, seq_len, seq_len)

last_layer_attn = outputs.attentions[-1]  # shape: (num_heads, seq_len, seq_len)
avg_head_attn = last_layer_attn.mean(dim=0)  # average across heads, shape: (seq_len, seq_len)

# Suppose we look at the last token's attention distribution to see which previous tokens guide it:
import numpy as np
guiding_tokens_scores = avg_head_attn[-1, :].cpu().numpy()  # attention to all previous tokens
sorted_indices = np.argsort(guiding_tokens_scores)[::-1]  # descending order

for idx in sorted_indices:
    print(f"Token: {tokenizer.decode(tokens[0][idx])}, Score: {guiding_tokens_scores[idx]:.4f}")
```

In an example related to “wokeness,” it wouldn’t be surprising if wokeness and its neighboring tokens in the input context get high attention scores. That’s a direct clue that the model is leaning heavily on that particular concept to guide the next word.

### Making It “Less Controversial”
You might wonder: “Is there a deterministic way to make this response less controversial?” A few strategies exist:

#### Prompt Engineering:
Add a system-level or prefix prompt that clarifies the tone or style. For example:

```python
prefix = "Please respond in a neutral, balanced manner. "
input_text = prefix + "These days wokeness has been a big "
```
This can shift the distribution of next tokens toward less extreme or polarizing ones.

#### Decoding Strategies:

Temperature: Lowering the temperature (closer to 0) makes the model more deterministic and less likely to produce outlier completions.
Top-p: Setting a lower top-p (nucleus sampling) will ignore low-probability tokens that might escalate controversy.

```python
output = model.generate(
    tokens,
    max_length=len(tokens[0]) + 10,
    do_sample=True,
    temperature=0.3,   # more deterministic
    top_p=0.8          # ignore less probable words
)
```

#### Lexical Penalties or Token Filtering:
You can manually reduce the logits for certain keywords or phrases you don’t want to appear in your completions. This approach gets more advanced, requiring direct manipulation of the model’s output distribution.

Example 3: A Happy Prompt
Let’s try something on the opposite end—lighthearted, “happy” content:

```python
input_text = "Today I feel so excited because "
input_text = "Today I feel so excited because "
tokens = tokenizer.encode(input_text, return_tensors="pt")

with torch.no_grad():
    output = model.generate(tokens, max_length=len(tokens[0]) + 7, do_sample=True, temperature=0.7)
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print("Input:", input_text)
print("Gemma-2b Output:", decoded_output)
```

Expect something like:

```yaml
Input: Today I feel so excited because
Gemma-2b Output: Today I feel so excited because I finally adopted a puppy!
```

The model’s next-token choice is guided by common everyday phrases that follow “excited because …”, often referencing life events like a new job, a puppy, meeting friends, etc.

### Mathematical Underpinnings: Vectors Galore!
Let’s get more concrete on the math. Every token is a vector 
𝑥
𝑡
x 
t
​
  in an embedding space of dimension 
  into 
ℎ
𝑡
(
𝑙
)
h 
t
(l)
​
  for layer 
𝑙
l:

ℎ
𝑡
(
𝑙
)
=
FFN
(
MHAttn
(
{
ℎ
1
(
𝑙
−
1
)
,
…
,
ℎ
𝑡
(
𝑙
−
1
)
}
)
)
h 
t
(l)
​
 =FFN(MHAttn({h 
1
(l−1)
​
 ,…,h 
t
(l−1)
​
 }))
where MHAttn is the multi-head attention that looks at all hidden states of the previous layer, and FFN is the feed-forward network. By layer 
𝐿
L, we have a contextual embedding 
ℎ
𝑡
(
𝐿
)
h 
t
(L)
​
  that is used to predict the next token distribution:

𝑃
(
token 
𝑣
∣
ℎ
𝑡
(
𝐿
)
)
  
=
  
S
o
f
t
m
a
x
(
𝑊
 
ℎ
𝑡
(
𝐿
)
)
P(token v∣h 
t
(L)
​
 )=Softmax(Wh 
t
(L)
​
 )
The attention mechanism includes queries, keys, and values. If you look at the attention scores:

Attn
(
𝑄
,
𝐾
,
𝑉
)
=
Softmax
(
𝑄
𝐾
⊤
𝑑
k
)
𝑉
Attn(Q,K,V)=Softmax( 
d 
k
​
 
​
 
QK 
⊤
 
​
 )V
the tokens with the highest 
𝑄
𝐾
⊤
𝑑
k
d 
k
​
 
​
 
QK 
⊤
 
​
  are the ones the model sees as relevant for the next output. That’s how “wokeness” might overshadow other tokens when dealing with the final prediction.

(Hypothetical) 2D Attention Heatmap
If we wanted an image of the attention from the last token to the entire context in that “wokeness” example, we might produce a 2D heatmap:

```perl

            "These"  "days"  "wokeness"  "has"  "been"  "a"  "big"
These         ...
days          ...
wokeness      ...
has           ...
been          ...
a             ...
big           ...
<next>       [0.1, 0.05, 0.3, 0.05, 0.02, 0.03, 0.45]  # hypothetical row
```

You might see the largest attention weight (0.45) on “big” and (0.3) on “wokeness” in the final row (the <next> token’s viewpoint). This matrix can be visualized in libraries like matplotlib’s imshow.

### Putting It All Together

#### Embeddings: Ground tokens in a high-dimensional space.
#### Attention: Guides the flow of contextual information. Certain tokens (like “wokeness”) can dominate attention, hence strongly influencing completions.
#### Logits & Sampling: The final distribution over next tokens is sampled (or greedily chosen) from. This is where temperature, top-k, top-p, and lexical penalties can shape the outcome.

### Key Takeaways:

#### Guiding Tokens: Typically the most relevant or unique tokens in the input. Investigating attention weights or gradient-based methods helps pinpoint these influences.
#### Reducing Controversy: Controlling model output can be done via prompt engineering, decoding strategies, or advanced logit manipulation.
#### Interpretability Tools: Visualizing attention, PCA projections, or even advanced interpretability methods (like activation patching or causal tracing) can shed light on exactly why Gemma-2b picks certain words.

### Conclusion
Working with a small LLM like Gemma-2b locally is a fantastic playground to learn how bigger models like GPT-4 or PaLM might behave under the hood. By experimenting with different prompts—ranging from the innocuous (“sun rises”) to the controversial (“wokeness”) to the joyful (“excited because…”)—we can see exactly how token embeddings, attention, and sampling come together to produce coherent text.

Armed with these insights, you can:

- Debug your LLM’s output.
- Optimize for certain styles or tones via prompt engineering.
- Understand which tokens are truly driving the generation process (the “guiding tokens”).

Happy experimenting, and may your explorations be forever guided by curiosity rather than controversy!

References & Further Reading:

- Attention Is All You Need (Vaswani et al., 2017)
- DistilGPT2 and interpretability frameworks: Hugging Face Docs
- Visualizing Attention: AllenNLP Interpret

Feel free to share any interesting completions or insights you discover while tinkering with Gemma-2b! -->
