## @package constants
#  This module provides physical constants in uniform format.

## [C], electron charge.
q_e = 1.60217662e-19

## [J * s], Planks constant.
h = 6.62e-34

## [m / s], speed of light.
c = 299792458

## [kg], electron mass.
m_e = 9.10938356e-31

## [m], electron radius
r_o = 2.8179403267e-15

## [K], room temperature
t_room = 273 + 23

## [J / K], Boltzmann constant
k_b = 1.38064852e-23

## Coverts pressure from [Torr] to [Pa]
def torr_to_pa(torr):
    return torr * 7.5006 * 1e-3


## floating point infinity
inf = float('inf')
