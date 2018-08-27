# Launching a Hadoop Cluster Using Docker

This guide describes how to pull and run a hadoop cluster using Docker. You can use this environment to get started on learning Hadoop, developing and testing your applications.

## What is Included:

- [hadoop-core](https://hub.docker.com/r/syan83/hadoop-core/):
	- Base Image: `ubuntu:16.04`
	- `JDK 1.8`
	- `Python 2.7.12`/`Python 3.5.2`
	- `Hadoop 2.8.4`

- [hadoop-stack](https://hub.docker.com/r/syan83/hadoop-stack/):
	- Base Image: `hadoop-core`
	- `MySQL: 5.7.23`
	- `Tez: 0.9.1`
	- `Hive: 2.3.3`
	- `Pig: 0.17.0`
	- `Sqoop: 1.4.7`
 
## Prerequisites:

Ensure that you have docker installed before you attempt running the command below.

To install the latest version of docker on your computer, please follow the instruction:

- Mac: [https://docs.docker.com/docker-for-mac/install/]()
- Windows: [https://docs.docker.com/docker-for-windows/install/]()


## Pseudo-Distributed Mode:

This section shows how to setup a single-node Hadoop cluster in docker. We will use the docker image `syan/hadoop-core` as an example. To use another image, simple replace `syan/hadoop-core` with the image's REPOSITORY or ID.

1. Open a terminal window (Mac: Terminal, Windows: PowerShell)
2. Pull the latest docker image:

	```
	docker pull syan83/hadoop-core
	```
	
	Once you have pulled the image, you should be able to see it's REPOSITORY, TAG, IMAGE ID, etc., from the list by running:
	
	```
	docker image ls
	```
	
3. Once you know the name or hash of the image, you can run it:

	```
	docker run -it \
        -p 8088:8088 \
        -p 19888:19888 \
        -p 50070:50070 \
        --name hadoop-core \
        syan83/hadoop-core
    ```
    
4. To mount a directory on the host machine into the cluster, run:

	```
	docker run -it \
        -p 8088:8088 \
        -p 19888:19888 \
        -p 50070:50070 \
        --name hadoop-core \
        --mount type=bind,source=<host dir path>,target=<container dir path> \
        syan83/hadoop-core
    ```
    
    For example, to mount a directory from your computer to the directory `/home/hadoop/examples` inside the container, first change your working directory into that directory, then run:
    
	```
	docker run -it \
        -p 8088:8088 \
        -p 19888:19888 \
        -p 50070:50070 \
        --name hadoop-core \
        --mount type=bind,source="$(pwd)",target=/home/hadoop/examples \
        syan83/hadoop-core
    ```

5. When you exit the cluster, the container is stopped, but not automatically removed. To clean up, run:

	```
	docker ps -aq --no-trunc -f status=exited | xargs docker rm
	```
	
