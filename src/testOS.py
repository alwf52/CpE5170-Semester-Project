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
        self.executable_jobs : list[Job] = []
        self.completed_jobs : list[Job] = []
        self.time = 0

# SCHEDULING ALGORITHMS --->
    def algorithm_edf(self) -> None:
        '''Performs the Earliest Deadline First scheduling algorithm on the set of jobs'''
        
        if not self.all_jobs_executeable():
            return
        
        self.sort_jobs_by_deadline()
        while len(self.jobs) > 0:
            self.get_executable_jobs()
            if len(self.executable_jobs) == 0:
                self.time += self.cpu_cycle
            # Assign jobs to idle CPU's
            for cpu in self.cpus:
                if cpu.current_job == None and self.one_cpu_per_job(cpu, self.executable_jobs[0]):
                    cpu.work_on(self.executable_jobs.pop(0))
            
            # Execute the current job on CPU
            for cpu in self.cpus:
                if cpu.execute():
                    self.completed_jobs.append(cpu.current_job)
                    self.jobs.remove(cpu.current_job)
                    cpu.job_completed()
            
            for cpu in self.cpus:
                print(self.jobs)
                print(cpu.graph)

            self.time += self.cpu_cycle


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
        for job in self.jobs:
            if job.t_release <= self.time:
                self.executable_jobs.append(job)

    def one_cpu_per_job(self, c : CPU,  j : Job) -> bool:
        '''Returns true if j is not being executed by another CPU'''
        for cpu in self.cpus:
            if cpu == c:
                continue
            if cpu.current_job == j:
                return False
            
        return True
# <--- UTILITY

# SORT JOBS --->
    def sort_jobs_by_deadline(self) -> None:
        jobs = self.jobs
        n = len(jobs)
        swapped = False

        for i in range(n - 1):
            for j in range(n - i - 1):
                if jobs[j].t_deadline > jobs[j + 1].t_deadline:
                    swapped = True
                    jobs[j], jobs[j + 1] = jobs[j + 1], jobs[j]

            if not swapped:
                return

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