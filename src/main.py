from testOS import OS

def main():
    os = OS(8)

    os.generate_random_jobs(8)
    print(os.jobs)
    os.algorithm_edf()
    print(os.sorted_jobs)

    for cpu in os.cpus:
        print(cpu.graph)

if __name__ == '__main__':
    main()