FROM registry.redhat.io/rhel8/python-36

LABEL description="Red Hat OpenStack Platform tempest"
LABEL summary="Red Hat OpenStack Platform tempest with nfv-plugin"
LABEL name="rhosp/openstack-tempest-nfv"


RUN pip3 install tempest-nfv-plugin python-tempestconf
RUN tempest init ~/tempest \
    && mkdir ~/tempest/container_tempest/

WORKDIR /opt/app-root/src/tempest


alias podman-tempest="podman run -i -v ./tempest.conf:/opt/app-root/src/tempest/etc/tempest.conf:z -v /home/stack/ci_network_config.yml:/opt/app-root/src/tempest/etc/ci_network_config.yml -v /home/stack/.ssh/id_rsa:/home/stack/.ssh/id_rsa:z localhost/tempest-v2 /bin/bash"