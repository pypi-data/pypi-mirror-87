# Big MOD

Nhập vào $3$ số nguyên $B$, $P$, $M$. Hãy tính:

$$R = B^P \mod M$$

## Input

- Dòng duy nhất chứa $3$ số nguyên không âm $B$, $P$ và $M$.

## Constraints

- $0 ≤ B, P ≤ 2^{31} - 1$
- $1 ≤ M ≤ 46340$

## Output

- $1$ số tự nhiên duy nhất $R$ là kết quả phép tính $R = B^P \mod M$


## Sample input 1

```
2 5 11
```

## Sample output 1

```
10
```

## Explanation 1

Vì $2^5 \mod 11 = 32 \mod 11 = 10$, nên ta có $R = 10$.


## Sample input 2

```
3 18132 17
```

## Sample output 2

```
13
```

