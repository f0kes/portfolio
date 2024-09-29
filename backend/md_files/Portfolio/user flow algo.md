I developed a data-driven algorithm to model and analyze user playtime shifts across different games. By comparing playtime snapshots at two distinct points, the algorithm calculates changes in individual game playtime, identifying where users have gained or lost time. It then redistributes these changes, mapping how lost playtime in certain games is reallocated to others where time has incresed.

The process aggregates user-level data into a global flow matrix, which provides a clear view of how gaming attention shifts across the community. This tool may help game developers and analysts track trends in user engagement, identify games gaining or losing traction, and derive insights into player behavior for strategic decision-making.

- for each user create a time delta vector D (for each game hour difference between earlier and latest snapshot). total gain is sum of all positive game deltas g. total loss is sum of all negative game deltas l
  $D_{i} = \textup{played }_{ i, now}-\textup{played }_{ i, last}$
  $g =\sum_{\substack{ D_i > 0}} D_i$
  $l =\sum_{\substack{ D_i < 0}} D_i$
  $v =min(|l|,|g|)$
- user flow table U (game,game) where 
  $U_{i,j} = v*(D_{j}/g) * (D_{i}/l)\leftarrow D_{i}<0 \textup{ and } D_{j}>0$
  $U_{i,j}=-U_{j,i}$
- global flow table F (game, game) is sum of all U tables