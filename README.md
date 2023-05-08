# tdgraphs
Python code for "Random processes for generating task-dependency graphs" by Jesse Geneson and Shen-Fu Tsai

We define and implement two random processes which can be combined to generate task-dependency graphs of order n with m edges and a specified number of initial vertices and terminal vertices:

In the (x, y) edge-removal process, we start with a maximally connected task-dependency graph and remove edges uniformly at random as long as they do not cause the number of initial vertices to exceed x or the number of terminal vertices to exceed y.

In the (x, y) edge-addition process, we start with an empty task-dependency graph and add edges uniformly at random as long as they do not cause the number of initial vertices to be less than x or the number of terminal vertices to be less than y.

In both processes we halt if there are exactly x initial vertices and y terminal vertices.

We ran trials for both processes to develop conjectures which appear in Section 4 of the paper.
