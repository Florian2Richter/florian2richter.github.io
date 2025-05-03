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

## Recap of Cellular Automata

As most people in the computer science world know, the smallest unit of state in a classical computer is a bit, which can take on just two values: 0 or 1. And yet, with just this minimal alphabet, we can encode all information—by stringing together long sequences of bits and storing them on hard drives or transmitting them over networks.

But the power of binary logic doesn't stop at information storage. Equally fundamental is the processing—or time evolution—of information, which underpins virtually all modern computing applications. The logic governing this evolution has become deeply complex. Take, for example, modern CPU architectures: they implement speculative execution and branch prediction, using past instruction patterns to guess future outcomes. These systems operate with layers of caching, parallelism, and dynamic scheduling, making the underlying logic incredibly intricate and often opaque.

In stark contrast stands the elegant simplicity of a *cellular automaton*: a rule that updates the state of a bit based solely on the states of its neighboring bits.

To illustrate the surprising richness of this simple concept, let us think it through. Starting with an elementary setup, we consider three bits at time $$t_0$$, say $$\{1, 0, 1\}$$, and map these to a single output bit at time $$t_1$$, i.e., 0 or 1. What is the degree of freedom we have in defining such a rule?

Three bits can represent $$2^3 = 8$$ different configurations. For each of these input configurations, we can independently choose an output bit—either 0 or 1. Therefore, the total number of distinct update rules is $$2^8 = 256$$.

![Wolfram Rule 150 visualization](/assets/images/wolfram_rule_150.svg)
*Figure 1: *




 Even this simple setup—like one bit looking at its immediate neighbors—already leads to 256 distinct patterns, known as the [elementary cellular automata](https://en.wikipedia.org/wiki/Elementary_cellular_automaton). Some of these generate trivial outcomes; others create fractal structures or chaotic patterns, all from basic local rules.

![Evolution of Rule 150 cellular automaton](/assets/images/full_ca_150.png)
*Figure 2: Time evolution of Rule 150 starting from a single active cell. Each row represents the state of the system at a successive time step, showing how complex patterns emerge from simple rules. This particular pattern exhibits fractal-like characteristics with triangular self-similar structures.*

So what happens if we try to translate this idea into the quantum world?
Can such rich complexity also emerge in systems governed by quantum rules?
Is there even a meaningful quantum analog of a cellular automaton—and what would it look like?



*[This is a template for your blog post. You can continue writing about cellular automata, their properties, and applications.]* 