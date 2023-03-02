from testOS import OS

def main():
    os = OS(2)

    os.generate_random_jobs(6)
    print(os.jobs)
    os.algorithm_edf()

    for cpu in os.cpus:
        print(cpu.graph)

if __name__ == '__main__':
    main()