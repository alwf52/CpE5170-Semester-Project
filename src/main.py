from scheduler import Scheduler

def main():
    scheduler = Scheduler(32)

    scheduler.generate_semi_random_jobs(200)
    scheduler.algorithm_edf()

if __name__ == '__main__':
    main()