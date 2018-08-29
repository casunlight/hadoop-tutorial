
# docker ps -aq --no-trunc -f status=exited | xargs docker rm
# Remove all stopped containers
docker rm $(docker ps -a -q)
# Remove all untagged images
docker rmi $(docker images -f "dangling=true" -q)

