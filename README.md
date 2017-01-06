# c2sdcc

(work in progress)
This tool is designed to convert C99-compatible source files to something closer to the dialect used by SDCC. 
For example, SDCC only allows declarations at the top of functions.

## Examples

Original:

```C
function example() {

  for (int i = 1; i != 42; i++) {
    int x = i * 3;
  }

}
```

Converted:

```C
function example() {
  int i;
  int x;

  for (i = 1; i != 42; i++) {
    x = i * 3;
  }

}
```
