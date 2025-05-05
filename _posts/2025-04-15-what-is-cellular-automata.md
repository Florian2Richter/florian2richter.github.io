---
layout: post
title: "1-D Symplectic Cellular Automata and its Application to Stabilizer States"
date: 2025-04-15
permalink: /2025/04/15/what-is-cellular-automata.html
categories: [qca, theory]
mathjax: true
---

## Overview
- 1-D Cellular Automata
- Linearity in 1-D
- Increasing State Space
- Symplectic Automata
- Stabilizer Codes
- Entanglement

## A Minimal Model of Computation: Cellular Automata

In classical computing, the smallest unit of state is the **bit**, which can take on just two values: 0 or 1. And yet, using only this minimal alphabet, we can encode all digital information—by arranging long sequences of bits and storing them on hard drives or transmitting them across networks.

But the power of binary logic extends beyond storage. Equally fundamental is the *processing* of information—its evolution over time—which underpins all modern computation. The logic that governs this evolution has grown extraordinarily complex. Consider today’s CPU architectures: they implement techniques like *speculative execution* and *branch prediction*, using past instruction patterns to anticipate future behavior. These systems are layered with caches, pipelines, parallelism, and dynamic scheduling, creating a highly intricate and often opaque web of computational processes.

In stark contrast stands the elegant minimalism of a **cellular automaton**: a system where each cell updates its state according to a simple, local rule.

### Single-Cell Automata

To build intuition for how information might evolve in such systems, let’s begin with the simplest case: a *single-cell automaton*, illustrated in Figure 1. While not a true cellular automaton—since it lacks spatial neighbors—this setup still provides a useful starting point.

Here, we evolve one time step by updating a bit \( b \) based solely on its current value, either 0 or 1.

![Single-cell cellular automaton](/assets/images/single_cell_CA.svg)  
*Figure 1: A single-cell automaton showing possible state transitions. The new state depends solely on the current state, via a simple update rule.*

How many such update rules exist? Since there are two possible input values (0 and 1), and each can be mapped independently to either 0 or 1, there are  
\[
2 \times 2 = 4
\]  
distinct rules:

1. Always output 0  
2. Always output 1  
3. Identity (output equals input)  
4. NOT (flip the bit)

None of these rules leads to a rich or chaotic time evolution. The most interesting behavior comes from the NOT rule, which causes the bit to oscillate between 0 and 1 at each time step.

Still, this simple setting introduces a convenient way to represent such rules—as a **bitstring** of length 2. The first bit encodes the output for input 1, the second for input 0. For example:

- The identity rule becomes `10`  
- The NOT rule becomes `01`  
- Constant 0: `00`  
- Constant 1: `11`

This compact representation allows us to label rules by their decimal equivalent, e.g., `10` → **Rule 2**, `01` → **Rule 1**, and so on. This same encoding approach generalizes to more complex automata, where longer bitstrings capture richer local configurations.



To illustrate the surprising richness of this deceptively simple setup, consider a one-dimensional array of bits—a lattice—where each bit updates based on a fixed local rule. Suppose we define a local update rule that maps three adjacent input bits at time $$t_0$$ to a single output bit at time $$t_1$$. For example, we consider a neighborhood $$(x\!-\!1,\, x,\, x\!+\!1)$$ and denote the corresponding bits at time $$t_0$$ as $$b^{(t_0)}_{x-1}, b^{(t_0)}_x, b^{(t_0)}_{x+1}$$. The rule then assigns an output bit $$b^{(t_1)}_x$$ based on this triplet.

How many distinct local rules can we define?

Each triplet of bits has $$2^3 = 8$$ possible configurations. For each of these 8 input combinations, the rule may independently specify an output bit—either 0 or 1. Thus, the total number of such local update rules is $$2^8 = 256$$. These 256 local rules define the class of *elementary cellular automata*.

A

Once the rule is fixed, we apply it across the entire lattice in a *translationally invariant* fashion: for each position $$x$$, the output bit at time $$t_1$$, denoted $$b^{(t_1)}_x$$, depends solely on the input bits $$b^{(t_0)}_{x-1}, b^{(t_0)}_x, b^{(t_0)}_{x+1}$$ (see Figure 1). Conceptually, this is akin to applying a 1D convolution kernel in machine learning—except that instead of computing a weighted sum, we apply a discrete, rule-based transformation.

![Local update rule applied to a bitstring](/assets/images/wolfram_rule_150.svg)  
*Figure 1: A single update step in an elementary cellular automaton. The three highlighted source bits at time $$t_0$$ form the local neighborhood that determines the output bit at position $$x$$ and time $$t_1$$.*

This *locality* and *uniformity*—each cell updating according to the same rule, based only on its immediate neighbors—are what make cellular automata so simple to define, yet so surprisingly rich in behavior. To see this in action, consider the full time evolution of Rule 150, starting from a single active cell. Each new row corresponds to a new time step, computed by repeatedly applying the local update rule discussed earlier. The resulting global pattern is shown in Figure 2.

![Evolution of Rule 150 cellular automaton](/assets/images/full_ca_150_evolution.png)  
*Figure 2: Time evolution of Rule 150 (bitstring: $$10010110$$) starting from a single active cell. Left: The first few time steps showing how the pattern begins to form from a single bit. Right: Extended evolution over hundreds of time steps revealing the emergent fractal structure with triangular self-similar patterns.*

What begins as a single bit eventually gives rise to a structure bearing striking resemblance to the [Sierpiński triangle](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle)—a classic fractal. This emergence of large-scale order from local, deterministic rules is a hallmark of cellular automata.

The 256 different [1D cellular automata](https://en.wikipedia.org/wiki/Elementary_cellular_automaton) have been extensively studied and serve as models for dynamics in diverse fields—from physics to biology to computer science. They are characterized by showing simple translations (named gliders), oscillations, fractals, and pure random behavior.

We now turn to a subset of these automata, which we will later generalize to explore applications in the theory of stabilizer states in quantum information.

## Linear Cellular Automata


*[This is a template for your blog post. You can continue writing about cellular automata, their properties, and applications.]* 