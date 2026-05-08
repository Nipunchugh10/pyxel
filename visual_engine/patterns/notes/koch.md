# Koch Snowflake

## Core Idea
The Koch snowflake is one of the earliest described fractal curves. It is built by iteratively replacing each line segment with four smaller segments.

## Mathematics
Each segment is divided into three equal parts. The middle part is replaced by two sides of an equilateral triangle pointing outwards.
- Length increase factor: $4/3$ per iteration.
- Total length at iteration $n$: $3 \cdot L \cdot (4/3)^n$, which diverges to infinity.

## Logic in Code
- A recursive function `get_koch_points` takes two points and a depth.
- It calculates the four sub-points and calls itself for the next depth level.
- Three such curves are joined to form a snowflake.

## Interesting Properties
- **Infinite Perimeter, Finite Area:** The snowflake has an infinite perimeter but fits within a finite circle.
