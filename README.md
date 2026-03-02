# Monoalphabetic Substitution Encoder/Decoder (CLI)

A small command-line tool to:
- **Encode** a text file using a monoalphabetic substitution key
- **Decode** a text file using either:
  - a provided key, or
  - an automatic key search (best-effort)

---

## Files you need

Put these files in the same folder as the script:

- `count_2l.txt`  (bigram counts)
- `count_3l.txt`  (trigram counts)

These are used to help the program guess a key when you decode without providing one.

---

## Install / Run

You only need Python 3.

Run the script like:

```bash
python main.py [options] <input_file> -o <output_file>
```

Example: Decoding a file with a provided key
```bash
python main.py -d -k "QWERTYUIOPASDFGHJKLZXCVBNM" encoded.txt -o decoded.txt
```

Example: Decoding a file without a key (automatic key search)
```bash
python main.py -d encoded.txt -o decoded.txt
```

### Future To Do List:
- [] Use longer n-grams (e.g. 4-grams, 5-grams) to potentially improve the quality of generated text.
- [] Optimize codebase (specifically the Steepest Ascent algorithm) to be more efficient and faster. 
- [] Increase diveristy of proposals for imrpovements when generating neighboring solutions in the Steepest Ascent algorithm.
- [] Use probabilities or noramalized log counts to evaluate key 
- [] My main goal is to implement a more advanced algorithm, ultilizing the Markov Chain Monte Carlo (MCMC) method, which is a more sophisticated approach for searching the key space than Steepest Ascent