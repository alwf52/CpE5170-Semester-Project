from scheduler import Scheduler

try:
    from terminaltables import AsciiTable
except:
    print("Please install the terminaltables addon with `pip install terminaltables`")
    print("or whatever you use to install python modules")
    exit(1)

def main():
    n_cpus = 3
    n_jobs = 20
    n_runs = 500

    scheduler = Scheduler(n_cpus)

    edf_misses = 0
    sjf_misses = 0
    lst_misses = 0
    fcfs_misses = 0
    for runs in range(n_runs):
        # Results saved in a graph for each algorithm
        edf_results : list[list[str]] = []
        sjf_results : list[list[str]] = []
        lst_results : list[list[str]] = []
        fcfs_results : list[list[str]] = []
        # Generate 10 random jobs for every run
        scheduler.generate_semi_random_jobs(n_jobs=n_jobs)

        print("EDF")
        edf_misses += scheduler.algorithm_edf()
        for i, cpu in enumerate(scheduler.cpus):
            edf_results.append([f"cpu-{i}"])
            edf_results[i].extend(cpu.graph)
        scheduler.reset_state() 

        print("SJF")
        sjf_misses += scheduler.algorithm_sjf()
        for i, cpu in enumerate(scheduler.cpus):
            sjf_results.append([f"cpu-{i}"])
            sjf_results[i].extend(cpu.graph)
        scheduler.reset_state()

        print("LST")
        lst_misses += scheduler.algorithm_lst()
        for i, cpu in enumerate(scheduler.cpus):
            lst_results.append([f"cpu-{i}"])
            lst_results[i].extend(cpu.graph)
        scheduler.reset_state()

        print("FCFS")
        fcfs_misses += scheduler.algorithm_fcfs()
        for i, cpu in enumerate(scheduler.cpus):
            fcfs_results.append([f"cpu-{i}"])
            fcfs_results[i].extend(cpu.graph)
        scheduler.reset_state()

        print("\nvvv RESULTS vvv\n")

        print("EDF RESULTS")
        table = AsciiTable(edf_results)
        table.inner_row_border = True
        print(table.table)

        print("SJF RESULTS")
        table = AsciiTable(sjf_results)
        table.inner_row_border = True
        print(table.table)

        print("LST RESULTS")
        table = AsciiTable(lst_results)
        table.inner_row_border = True
        print(table.table)

        print("FCFS RESULTS")
        table = AsciiTable(fcfs_results)
        table.inner_row_border = True
        print(table.table)
    
    print("\nVVV MISSES VVV\n")

    print("AVG EDF MISSES")
    print(edf_misses / n_runs)

    print("AVG SJF MISSES")
    print(sjf_misses / n_runs)

    print("AVG LST MISSES")
    print(lst_misses / n_runs)

    print("AVG FCFS MISSES")
    print(fcfs_misses / n_runs)
    input()

if __name__ == '__main__':
    main()