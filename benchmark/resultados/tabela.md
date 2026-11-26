Tempos em segundos.

| Algoritmo | 1000 alea. | 1000 orde. | 1000 inve. | 10000 alea. | 10000 orde. | 10000 inve. | 50000 alea. | 50000 orde. | 50000 inve. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bubble | 0.057772 | 0.000090 | 0.064263 | 6.901646 | 0.000853 | 7.531221 | 220.706788 | 0.004342 | 174.745584 |
| selection | 0.041268 | 0.041188 | 0.058869 | 4.510738 | 4.243370 | 4.317724 | 181.397679 | 88.864906 | 90.790805 |
| insertion | 0.020473 | 0.000118 | 0.064586 | 2.086543 | 0.001226 | 4.578154 | 83.509234 | 0.006342 | 95.410643 |
| quick | 0.001436 | 0.000797 | 0.001247 | 0.016589 | 0.009541 | 0.010121 | 0.191666 | 0.056013 | 0.056139 |
| merge | 0.001543 | 0.001200 | 0.001807 | 0.021225 | 0.015136 | 0.016412 | 0.189239 | 0.161402 | 0.107487 |

Razão de crescimento (medido × teórico)

| Algoritmo | Cenário | n1 → n2 | Medido | Teórico (médio/pior) |
|---|---|---|---:|---:|
| bubble | aleatoria | 1000 → 10000 | 119.5x | 100.0x |
| bubble | aleatoria | 10000 → 50000 | 32.0x | 25.0x |
| bubble | ordenada | 1000 → 10000 | 9.5x | 100.0x |
| bubble | ordenada | 10000 → 50000 | 5.1x | 25.0x |
| bubble | inversa | 1000 → 10000 | 117.2x | 100.0x |
| bubble | inversa | 10000 → 50000 | 23.2x | 25.0x |
| selection | aleatoria | 1000 → 10000 | 109.3x | 100.0x |
| selection | aleatoria | 10000 → 50000 | 40.2x | 25.0x |
| selection | ordenada | 1000 → 10000 | 103.0x | 100.0x |
| selection | ordenada | 10000 → 50000 | 20.9x | 25.0x |
| selection | inversa | 1000 → 10000 | 73.3x | 100.0x |
| selection | inversa | 10000 → 50000 | 21.0x | 25.0x |
| insertion | aleatoria | 1000 → 10000 | 101.9x | 100.0x |
| insertion | aleatoria | 10000 → 50000 | 40.0x | 25.0x |
| insertion | ordenada | 1000 → 10000 | 10.4x | 100.0x |
| insertion | ordenada | 10000 → 50000 | 5.2x | 25.0x |
| insertion | inversa | 1000 → 10000 | 70.9x | 100.0x |
| insertion | inversa | 10000 → 50000 | 20.8x | 25.0x |
| quick | aleatoria | 1000 → 10000 | 11.6x | 13.3x |
| quick | aleatoria | 10000 → 50000 | 11.6x | 5.9x |
| quick | ordenada | 1000 → 10000 | 12.0x | 13.3x |
| quick | ordenada | 10000 → 50000 | 5.9x | 5.9x |
| quick | inversa | 1000 → 10000 | 8.1x | 13.3x |
| quick | inversa | 10000 → 50000 | 5.5x | 5.9x |
| merge | aleatoria | 1000 → 10000 | 13.8x | 13.3x |
| merge | aleatoria | 10000 → 50000 | 8.9x | 5.9x |
| merge | ordenada | 1000 → 10000 | 12.6x | 13.3x |
| merge | ordenada | 10000 → 50000 | 10.7x | 5.9x |
| merge | inversa | 1000 → 10000 | 9.1x | 13.3x |
| merge | inversa | 10000 → 50000 | 6.5x | 5.9x |
