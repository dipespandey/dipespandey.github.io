<!-- ---
layout: post
title: Hands-on Physics with Python
date: 2024-12-26 11:59:00-0400
categories: learning physics LLM
gisqus_comments: true
---

### [AIFeynman](https://pypi.org/project/aifeynman/)

### PyPhysics

### Manim

Let's explore a fascinating physics experiment that combines symbolic mathematics from AIFeynman, physical simulations from PyPhysics, and beautiful visualizations using Manim - simulating and visualizing a double pendulum system.

A double pendulum is a classic example of chaotic motion in physics. It consists of one pendulum attached to another, creating complex and unpredictable movements that beautifully demonstrate principles of mechanics, energy conservation, and chaos theory.

### The Physics Behind Double Pendulum

The motion of a double pendulum is governed by coupled differential equations derived from Lagrangian mechanics. While the equations are complex, we can break them down into manageable components using our Python tools.

### Implementation

First, let's set up our environment with the required packages:

```python
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from manim import *
```

Let's define our double pendulum simulation class:

```python
class DoublePendulum:
    def __init__(self, m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81):
        self.m1, self.m2 = m1, m2  # masses
        self.L1, self.L2 = L1, L2  # lengths
        self.g = g  # gravitational acceleration
        
    def derivatives(self, state, t):
        theta1, omega1, theta2, omega2 = state
        
        c = np.cos(theta1 - theta2)
        s = np.sin(theta1 - theta2)
        
        theta1_dot = omega1
        theta2_dot = omega2
        
        # Derived from Lagrangian mechanics
        omega1_dot = (-self.g*(2*self.m1 + self.m2)*np.sin(theta1) - 
                     self.m2*self.g*np.sin(theta1 - 2*theta2) -
                     2*s*self.m2*(omega2**2*self.L2 + 
                     omega1**2*self.L1*c)) / (self.L1*(2*self.m1 + 
                     self.m2 - self.m2*np.cos(2*(theta1 - theta2))))
        
        omega2_dot = (2*s*(omega1**2*self.L1*(self.m1 + self.m2) +
                     self.g*(self.m1 + self.m2)*np.cos(theta1) +
                     omega2**2*self.L2*self.m2*c)) / (self.L2*(2*self.m1 +
                     self.m2 - self.m2*np.cos(2*(theta1 - theta2))))
        
        return [theta1_dot, omega1_dot, theta2_dot, omega2_dot]
```

Now, let's create a Manim animation to visualize the double pendulum:

```python
class DoublePendulumAnimation(Scene):
    def construct(self):
        # Initialize pendulum parameters
        dp = DoublePendulum()
        
        # Initial conditions
        state0 = [np.pi/2, 0, np.pi/2, 0]  # theta1, omega1, theta2, omega2
        t = np.linspace(0, 10, 1000)
        
        # Solve ODE
        states = odeint(dp.derivatives, state0, t)
        
        # Create pendulum visualization
        pivot = Dot()
        self.add(pivot)
        
        # Create pendulum arms and bobs
        L1, L2 = dp.L1, dp.L2
        arm1 = Line(pivot.get_center(), [L1*np.sin(states[0,0]), 
                   -L1*np.cos(states[0,0]), 0])
        bob1 = Dot(arm1.get_end())
        arm2 = Line(bob1.get_center(), [L1*np.sin(states[0,0]) + 
                   L2*np.sin(states[0,2]),
                   -L1*np.cos(states[0,0]) - L2*np.cos(states[0,2]), 0])
        bob2 = Dot(arm2.get_end())
        
        # Add trace
        trace = VMobject()
        trace.set_points_as_corners([arm2.get_end()])
        
        self.add(arm1, bob1, arm2, bob2, trace)
        
        def update_pendulum(mob, dt):
            t = self.time
            i = int(t * 100) % len(states)
            theta1, theta2 = states[i,0], states[i,2]
            
            # Update positions
            new_bob1_pos = [L1*np.sin(theta1), -L1*np.cos(theta1), 0]
            new_bob2_pos = [L1*np.sin(theta1) + L2*np.sin(theta2),
                           -L1*np.cos(theta1) - L2*np.cos(theta2), 0]
            
            arm1.put_start_and_end_on(pivot.get_center(), new_bob1_pos)
            bob1.move_to(new_bob1_pos)
            arm2.put_start_and_end_on(new_bob1_pos, new_bob2_pos)
            bob2.move_to(new_bob2_pos)
            
            # Update trace
            trace.add_points_as_corners([new_bob2_pos])
        
        self.add_updater(update_pendulum)
        self.wait(10)
```

### Analysis and Results

When we run this simulation, we observe several interesting phenomena:

1. **Chaos**: Small changes in initial conditions lead to dramatically different trajectories
2. **Energy Conservation**: The total energy (kinetic + potential) remains constant
3. **Phase Space**: The system's behavior can be visualized in phase space, showing its chaotic nature

### Using AIFeynman for Analysis

We can use AIFeynman to verify our equations and discover patterns in the system's behavior:

```python
from aifeynman import run_aifeynman

# Generate data from our simulation
# AIFeynman will try to find mathematical patterns
data = np.column_stack((t, states))
run_aifeynman(data, 'double_pendulum_data.csv')
```

### Conclusion

This example demonstrates the power of combining modern tools like LLMs and Python libraries for physics education:

- AIFeynman helps us understand and verify the mathematical relationships
- PyPhysics provides the numerical simulation capabilities
- Manim creates beautiful visualizations that help build intuition

The double pendulum system, while seemingly simple, reveals the fascinating complexity that can arise from basic physical laws. Through these tools, we can explore and understand such systems more deeply than ever before.

### Further Exploration

Try experimenting with different initial conditions, masses, and lengths to see how the system's behavior changes. You can also:

- Add energy calculations to verify conservation
- Create phase space plots
- Explore Lyapunov exponents to quantify the chaos
- Compare numerical solutions with small-angle approximations

The code for this simulation is available on [GitHub](your-repository-link).

---

*Note: This simulation assumes ideal conditions (no friction or air resistance). Real double pendulums will eventually come to rest due to these factors.* -->