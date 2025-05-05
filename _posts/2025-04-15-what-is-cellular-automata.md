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

But the power of binary logic extends beyond storage. Equally fundamental is the *processing* of information—its evolution over time—which underpins all modern computation. The logic that governs this evolution has grown extraordinarily complex. Consider today's CPU architectures: they implement techniques like *speculative execution* and *branch prediction*, using past instruction patterns to anticipate future behavior. These systems are layered with caches, pipelines, parallelism, and dynamic scheduling, creating a highly intricate and often opaque web of computational processes.

In stark contrast stands the elegant minimalism of a **cellular automaton**: a system where each cell updates its state according to a simple, local rule.

### Single-Cell Automata

To build intuition for how information might evolve in such systems, let's begin with the simplest case: a *single-cell automaton*, illustrated in Figure 1. While not a true cellular automaton—since it lacks spatial neighbors—this setup still provides a useful starting point to introduce some notation.

Here, we evolve one time step by updating a bit $$b^{t=0}$$ based solely on its current value, either 0 or 1.

![Single-cell cellular automaton](/assets/images/single_cell_CA.svg)  
*Figure 1: A single-cell automaton showing possible state transitions. The new state depends solely on the current state, via a simple update rule.*

How many such different possibilities for time-step rules exist? Since there are two possible input values (0 and 1), and each can be mapped independently to either 0 or 1, there are  
\[
$$2 \times 2 = 4$$
\]  
distinct rules:

1. Always output 0  
2. Always output 1  
3. Identity (output equals input)  
4. NOT (flip the bit)

Not very surprisingly, none of these rules leads to a rich time evolution. Still, the most "interesting" behavior comes from the NOT rule, which causes the bit to oscillate between 0 and 1 at each time step.

Let us take the opportunity to introduce a convenient way to represent such rules—as a **bitstring** that uniquely determines the automaton's behavior. Consider the first bit of the string as the output for the input value 1, and the second bit as the output for input value 0. This results in the following representation of all four automata:

- Identity rule: `10`  
- NOT rule: `01`  
- Constant 0: `00`  
- Constant 1: `11`

Now, we find a nice way to not just count all possible automata, but also assign them names, e.g., `10` → **Rule 2**, `01` → **Rule 1**, and so on. This same encoding approach generalizes to more complex automata, where longer bitstrings capture richer local configurations.

To obtain richer dynamics, we obviously have to allow for more degrees of freedom. One possible way would be to introduce a longer "memory" to our dynamics, i.e., conditioning the state at the next time step on more than just the previous value. However, a more natural choice is to consider more than just a single cell as input for the update. This brings in some beautiful complexity, as we will see in the next chapter.

### Wolfram's Cellular Automata

Before we define update rules with multiple input bits, let us briefly introduce two key principles: **translational invariance** and **locality**. A rule is translationally invariant if it applies uniformly across space—that is, the same logic governs the evolution of every cell, regardless of its position. Locality, on the other hand, means that the state of each cell at the next time step depends only on a limited neighborhood around it, not on distant parts of the system. Conceptually, this is very similar to applying a 1D convolution kernel in machine learning—except that instead of computing a weighted sum, we apply a discrete, rule-based transformation.

These two ideas together allow us to scale from a single-bit system to a structured array of bits—like a line of cells—where each cell evolves by the same simple rule, based only on nearby information. This setting defines the simplest spatially extended version of a cellular automaton: a one-dimensional lattice of bits with local update rules applied in parallel.

To illustrate the surprising richness of this deceptively simple setup, consider a one-dimensional array of bits—a lattice—where each bit updates based on a fixed local rule. Suppose we define a local update rule that maps three adjacent input bits at time $$t_0$$ to a single output bit at time $$t_1$$. For example, we consider a neighborhood $$(x\!-\!1,\, x,\, x\!+\!1)$$ and denote the corresponding bits at time $$t_0$$ as $$b^{(t_0)}_{x-1}, b^{(t_0)}_x, b^{(t_0)}_{x+1}$$. The rule then assigns an output bit $$b^{(t_1)}_x$$ based on this triplet (see Figure 2).

How many distinct local rules can we define?

Each triplet of bits has $$2^3 = 8$$ possible configurations. For each of these 8 input combinations, the rule may independently specify an output bit—either 0 or 1. Thus, the total number of such local update rules is $$2^8 = 256$$. These 256 local rules define the famous class of *elementary cellular automata* investigated by Stephen Wolfram.

![Local update rule applied to a bitstring](/assets/images/wolfram_rule_150.svg)  
*Figure 2: A single update step in an elementary cellular automaton. The three highlighted source bits at time $$t_0$$ form the local neighborhood that determines the output bit at position $$x$$ and time $$t_1$$.*

To see the rich dynamics in action, consider the full time evolution of Rule 150, starting from a single active cell (Figure 3). Each new row corresponds to a new time step (time is plotted downwards), computed by repeatedly applying the local update rule discussed earlier.

![Evolution of Rule 150 cellular automaton](/assets/images/full_ca_150_evolution.png)  
*Figure 3: Time evolution of Rule 150 (bitstring: $$10010110$$) starting from a single active cell. Left: The first few time steps showing how the pattern begins to form from a single bit. Right: Extended evolution over hundreds of time steps revealing the emergent fractal structure with triangular self-similar patterns.*

What begins as a single bit eventually gives rise to a structure bearing a striking resemblance to the [Sierpiński triangle](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle)—a classic fractal. This emergence of large-scale order from local, deterministic rules is a hallmark of cellular automata.

The 256 different [1D cellular automata](https://en.wikipedia.org/wiki/Elementary_cellular_automaton) have been extensively studied and serve as models for dynamics in diverse fields—from physics to biology to computer science. They are characterized by simple translations (called *gliders*), oscillations, fractals, and pure random behavior.

We now turn to a subset of these automata, which we will later generalize to explore applications in the theory of stabilizer states in quantum information.