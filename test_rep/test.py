from semanphone import semanphone


alpha = 0.95

filename = "random_words_50"
output_file = 'alpha' + str(alpha)


with open(filename, 'r') as f:
    results = {word: semanphone(word.strip()) for word in f}
    with open(output_file, 'w+') as output:
        for k, v in results.items():
            output.write(' '.join([k.strip()] + [x[0] for x in v]))
            output.write('\n')

    print(output_file + " was generated successfully!")