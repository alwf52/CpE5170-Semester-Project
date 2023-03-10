from testOS import OS

def main():
    os = OS(32)

    os.generate_semi_random_jobs(200)
    os.algorithm_edf()

    

if __name__ == '__main__':
    main()