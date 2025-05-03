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

In classical computing, the smallest unit of state is the bit, which can take on just two values: 0 or 1. And yet, with just this minimal alphabet, we can encode all information—by stringing together long sequences of bits and storing them on hard drives or transmitting them over networks.

But the power of binary logic doesn't stop at information storage. Equally fundamental is the *processing* of information—its time evolution—which underpins virtually all modern computation. The logic governing this evolution has become deeply complex. Take, for example, modern CPU architectures: they implement speculative execution and branch prediction, using past instruction patterns to guess future outcomes. These systems operate with layers of caching, parallelism, and dynamic scheduling, making the underlying logic incredibly intricate and often opaque.

In stark contrast stands the elegant simplicity of a *cellular automaton*: a rule that updates the state of a bit based solely on the states of its neighboring bits.

To illustrate the surprising richness of this deceptively simple setup, consider a one-dimensional array of bits—a lattice—where each bit updates based on a fixed local rule. Suppose we define a local update rule that maps three adjacent input bits at time $$t_0$$ to a single output bit at time $$t_1$$. For example, we consider a neighborhood $$(x\!-\!1,\, x,\, x\!+\!1)$$ and denote the corresponding bits at time $$t_0$$ as $$b^{(t_0)}_{x-1}, b^{(t_0)}_x, b^{(t_0)}_{x+1}$$. The rule then assigns an output bit $$b^{(t_1)}_x$$ based on this triplet.

How many distinct local rules can we define?

Each triplet of bits has $$2^3 = 8$$ possible configurations. For each of these 8 input combinations, the rule may independently specify an output bit—either 0 or 1. Thus, the total number of such local update rules is $$2^8 = 256$$. These 256 local rules define the class of *elementary cellular automata*.

A convenient way to represent such a rule is as a bitstring of length 8, where each position encodes the output associated with one of the 8 input configurations (ordered, for instance, lexicographically from $$111$$ down to $$000$$). This encoding allows us to label rules by an integer from 0 to 255—the decimal value of the bitstring. For instance, Rule 110 corresponds to the bitstring $$01101110$$.

Once the rule is fixed, we apply it across the entire lattice in a *translationally invariant* fashion: for each position $$x$$, the output bit at time $$t_1$$, denoted $$b^{(t_1)}_x$$, depends solely on the input bits $$b^{(t_0)}_{x-1}, b^{(t_0)}_x, b^{(t_0)}_{x+1}$$ (see Figure 1). Conceptually, this is akin to applying a 1D convolution kernel in machine learning—except that instead of computing a weighted sum, we apply a discrete, rule-based transformation.

![Local update rule applied to a bitstring](/assets/images/wolfram_rule_150.svg)  
*Figure 1: A single update step in an elementary cellular automaton. The three highlighted source bits at time $$t_0$$ form the local neighborhood that determines the output bit at position $$x$$ and time $$t_1$$.*

This *locality* and *uniformity*—each cell updating according to the same rule, based only on its immediate neighbors—are what make cellular automata so simple to define, yet so surprisingly rich in behavior. To see this in action, consider the full time evolution of Rule 150, starting from a single active cell. Each new row corresponds to a new time step, computed by repeatedly applying the local update rule discussed earlier. The resulting global pattern is shown in Figure 2.

![Evolution of Rule 150 cellular automaton](/assets/images/full_ca_150_evolution.png)  
*Figure 2: Time evolution of Rule 150 (bitstring: $$10010110$$) starting from a single active cell. Left: The first few time steps showing how the pattern begins to form. Right: Extended evolution over hundreds of time steps revealing the emergent fractal structure with triangular self-similar patterns.*

What begins as a single bit eventually gives rise to a structure bearing striking resemblance to the [Sierpiński triangle](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle)—a classic fractal. This emergence of large-scale order from local, deterministic rules is a hallmark of cellular automata.

The 256 different [1D cellular automata](https://en.wikipedia.org/wiki/Elementary_cellular_automaton) have been extensively studied and serve as models for dynamics in diverse fields—from physics to biology to computer science. They are characterized by showing simple translations (named gliders), oscillations, fractals, and pure random behavior.

We now turn to a subset of these automata, which we will later generalize to explore applications in the theory of stabilizer states in quantum information.

## Linear Cellular Automata


*[This is a template for your blog post. You can continue writing about cellular automata, their properties, and applications.]* 