# TrapezoidalMaps

This program creates a trapezoidal map for given input line segments by building a rooted directed acyclic graph under the constraint that no two input points lie on the same vertical line. The program then generates <i>true</i> trapezoids such that they are either quadrangles with two parallel vertical sides or triangles.

The following diagram shows the resulting trapezoidal map for line segments represented by the 7 endpoints, from P1, P2, P3, P4, and Q1, Q2, Q4.

The final map contains 12 trapezoids, namely T1, …, T12. As shown, the points Q1 and Q3 are coincidental and the resulting effect is shown in the sketch as well as the later graph representation.

<p align="center">
	<img src="https://github.com/ad8454/TrapezoidalMaps/blob/master/tZMap.PNG" width="600">
  <div align="center"><i><b>Trapezoidal Map</b></i></div>
</p>



The following is the representation of the Rooted Directed Acyclic Graph for the adjacency matrix that is created for the above map.

<p align="center">
	<img src="https://github.com/ad8454/TrapezoidalMaps/blob/master/graph.PNG" width="600">
  <div align="center"><i><b>Rooted DAG</b></i></div>
</p>
