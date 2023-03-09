from cpu import CPU
from job import Job
from random import randint

class OS:
    def __init__(self, n_cpus : int = 1, time_step : float = 1) -> None:
        # How many cpu's does the OS have
        self.cpu_count = n_cpus
        # How much of a task is completed every cycle
        self.cpu_cycle = time_step

        self.cpus : list[CPU] = []
        for n in range(self.cpu_count):
            self.cpus.append(CPU(f"cpu-{n}", self.cpu_cycle))

        self.jobs : list[Job] = []
        self.sorted_jobs : list[Job] = []
        self.executable_jobs : list[Job] = []
        self.completed_jobs : list[Job] = []
        self.time = 0

# SCHEDULING ALGORITHMS --->
    def algorithm_edf(self) -> None:
        '''Performs the Earliest Deadline First scheduling algorithm on the set of jobs'''
        
        # If the set of jobs have deadlines that cannot be met with the same number of CPU's
        if not self.all_jobs_executeable():
            return
        
        self.sort_jobs_by_deadline()
        while len(self.completed_jobs) != len(self.jobs):
            self.get_executable_jobs()
            if len(self.executable_jobs) == 0:
                self.time += self.cpu_cycle

            # Assign jobs to idle CPU's
            for cpu in self.cpus:
                if len(self.executable_jobs) == 0:
                    continue

                for job in self.executable_jobs:
                    if len(self.executable_jobs) > 0 and cpu.current_job == None and self.one_cpu_per_job(cpu, self.executable_jobs[0]):
                        cpu.work_on(self.executable_jobs.pop(self.executable_jobs.index(job)))  

            # Execute the current job on CPU
            for cpu in self.cpus:
                # If a job is completed
                if cpu.execute():
                    self.completed_jobs.append(cpu.current_job)
                    self.sorted_jobs[self.sorted_jobs.index(cpu.current_job)].t_finish = self.time
                    # self.jobs.remove(cpu.current_job)
                    cpu.job_completed()

            self.time += self.cpu_cycle

        misses : list[str] = []
        for job in self.jobs:
            if job.t_deadline - job.t_finish < 0:
                misses.append(job.name)
        
        if len(misses) > 0:
            print(f"{len(misses)} job(s) have missed their deadline")
            print("Missed jobs: ", end='')
            for job in misses:
                print(job, end=', ')
            print()
        



    def algorithm_rr(self) -> None:
        pass

    def algorithm_lst(self) -> None:
        pass
# <--- SCHEDULING ALGORITHMS

# UTILITY --->
    def all_jobs_executeable(self) -> bool:
        if len(self.jobs) == 0:
            print("No jobs to test")
            return False

        for job in self.jobs:
            if job.t_release + job.t_execution > job.t_deadline:
                print(f"Job {job} cannot be executed!!!")
                return False
        return True
    
    def get_executable_jobs(self) -> bool:
        self.executable_jobs = []
        for job in self.sorted_jobs:
            # If a job is currently executing on a CPU, don't include it in executable jobs
            currently_executing = True
            for cpu in self.cpus:
                if self.one_cpu_per_job(cpu, job):
                    currently_executing = False

            if job.t_release <= self.time and job not in self.completed_jobs and not currently_executing:
                self.executable_jobs.append(job)

    def one_cpu_per_job(self, c : CPU,  j : Job) -> bool:
        '''Returns true if j is not being executed by another CPU'''
        for cpu in self.cpus:
            if cpu == c:
                continue
            if cpu.current_job and cpu.current_job.name == j.name:
                return False
            
        return True
# <--- UTILITY

# SORT JOBS --->
    def sort_jobs_by_deadline(self) -> None:
        sorted_jobs = self.jobs.copy()
        n = len(sorted_jobs)
        swapped = False

        for i in range(n - 1):
            for j in range(n - i - 1):
                if sorted_jobs[j].t_deadline > sorted_jobs[j + 1].t_deadline:
                    swapped = True
                    sorted_jobs[j], sorted_jobs[j + 1] = sorted_jobs[j + 1], sorted_jobs[j]

            if not swapped:
                return
            
        self.sorted_jobs = sorted_jobs

    def sort_jobs_by_execution(self) -> None:
        jobs = self.jobs
        n = len(jobs)
        swapped = False

        for i in range(n - 1):
            for j in range(n - i - 1):
                if jobs[j].t_execution > jobs[j + 1].t_execution:
                    swapped = True
                    jobs[j], jobs[j + 1] = jobs[j + 1], jobs[j]

            if not swapped:
                return
            
    def sort_jobs_by_slack(self) -> None:
        jobs = self.jobs
        n = len(jobs)
        swapped = False

        for i in range(n - 1):
            for j in range(n - i - 1):
                if jobs[j].calculate_slack(self.time) > jobs[j + 1].calculate_slack(self.time):
                    swapped = True
                    jobs[j], jobs[j + 1] = jobs[j + 1], jobs[j]

            if not swapped:
                return
# <--- SORT JOBS

# GENERATE JOBS --->
    def generate_jobs_from_file(self, file : str) -> None:
        self.jobs = []
        with open(file) as f:
            n = -1
            for line in f:
                n += 1
                red = line.split()
                if len(red) != 3:
                    print("Invalid file format, lines should look like -> r e d -> 0 1 5")
                    self.jobs = []
                    return
                self.jobs.append(Job(red[0], red[1], red[2], f"J{n}"))

    def generate_random_jobs(self, n_jobs : int) -> None:
        # Clear jobs
        self.jobs = []
        for n in range(n_jobs):
            # Semi random jobs
            r = self.cpu_cycle * randint(0, n + 1)
            e = self.cpu_cycle * randint(1, n_jobs)
            d = r + e + self.cpu_cycle * randint(0, n_jobs)
            self.jobs.append(Job(r, e, d, f"J{n}"))
# <--- GENERATE JOBS