def write_to_file(name: str, avg_pd: float):
    with open(name, 'a+') as file:
        line = str(avg_pd) + "\n"
        file.write(line)
