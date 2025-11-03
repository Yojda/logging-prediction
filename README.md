**logging-prediction** is a AIOps model that uses machine learning to predict fault via logs.

The project is created by Yannis Ouakrim in the context of his master's degree in Software Engineering at École de Technologie Supérieure (ÉTS) in Montreal, Canada.

### Dependencies

logging-prediction requires:

- python (3.11)
- logparser3
- matplotlib
- jupyter

### Installation

To install logging-prediction, clone the repository and install the required dependencies:

```bash
git clone git@github.com:Yojda/defect-prediction.git
```

### Usage

To use logging-prediction, run the training jupyter notebook with the desired parameters:

```bash
jupyter lab
```

Then open the `training.ipynb` notebook and follow the instructions to train and evaluate the model.

### Development

#### Linux system log

[Linux](https://github.com/logpai/loghub/tree/master/Linux) logs are usually located at `/var/log/`. The dataset was collected from `/var/log/messages` on a Linux server over a period of 260+ days, as part of the Public Security Log Sharing Site project.

```
Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
```

- Timestamp `Jun 14 15:16:01`
- Hostname `combo`
- Service/Application name `sshd(pam_unix)[19939]`, where `sshd` is the service name, `pam_unix` is the module name, and `19939` is the PID.
- Message `authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4`

There are various types of log messages, including:
- Authentication failures `Authentication failed from <*> (<*>): Permission denied in replay cache code`
- System errors `There is already a security framework initialized, register_security failed.`
- Service start/stop events `HCI daemon ver <*>.<*> started`

#### OpenStack infrastructure log

[OpenStack](https://github.com/logpai/loghub/tree/master/OpenStack) is a cloud operating system that controls large pools of compute, storage, and networking resources throughout a datacenter. This dataset was generated on CloudLab, a flexible, scientific infrastructure for research on cloud computing. Both normal logs and abonormal cases with failure injection are provided, making the data amenable to anomaly detection research.

```
nova-api.log.1.2017-05-16_13:53:08 2017-05-16 00:00:00.008 25746 INFO nova.osapi_compute.wsgi.server [req-38101a0b-2096-447d-96ea-a692162415ae 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] 10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1893 time: 0.2477829
```

- Log filename `nova-api.log.1.2017-05-16_13:53:08`
- Timestamp `2017-05-16 00:00:00.008`
- PID `25746`
- Log level `INFO`
- Component `nova.osapi_compute.wsgi.server`
- ADDR `[req-38101a0b-2096-447d-96ea-a692162415ae 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -]`
- Message `10.11.10.1 "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1" status: 200 len: 1893 time: 0.2477829`

There are various types of log messages, including:
- API requests `<*> "GET <*>" status: <*> len: <*> time: <*>.<*>`
- CRUD operations on instances `[instance: <*>] Deleting instance files <*>`
- VM actions `[instance: <*>] VM Paused (Lifecycle Event)`
