#write the output of the command nvidia-smi --query-gpu "timestamp","index","name","pci.bus_id","utilization.gpu","utilization.memory","memory.used","memory.free","memory.total" --format=csv to a file called gpu_usage.csv

nvidia-smi --query-gpu "timestamp","index","name","pci.bus_id","utilization.gpu","utilization.memory","memory.used","memory.free","memory.total" --format=csv >> gpu_usage.csv
