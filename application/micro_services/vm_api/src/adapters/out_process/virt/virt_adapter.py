import subprocess
import os
import libvirt
import xml.etree.ElementTree as ET
from fastapi import HTTPException
from application.ports.vm_ports.vm_creator import VMCreatorPort
from domain.models.vm_models.vm_model import VMCreateRequest
from application.ports.vm_ports.vm_remover import VMRemoverPort
from application.ports.vm_ports.vm_fetcher import VMFetcherPort
from domain.models.vm_models.vm_details import VMDetailedInfo

class VirtInstallVMCreator(VMCreatorPort):
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir

    def create(self, vm_request: VMCreateRequest):
        # Generate ks.cfg
        template_file = os.path.join(self.templates_dir, f"{vm_request.template_name}.cfg")
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"Template {vm_request.template_name}.cfg does not exist.")

        with open(template_file, "r") as f:
            ks_template = f.read()

        ks_config = ks_template.format(**vm_request.dict())
        ks_cfg_path = os.path.join(self.templates_dir, "ks.cfg")

        with open(ks_cfg_path, "w") as f:
            f.write(ks_config)

        # Command to create the virtual machine
        command = [
            "virt-install",
            "--memory", str(vm_request.RAM),
            "--vcpus", str(vm_request.CPU),
            "--location", "/var/lib/libvirt/boot/Rocky-8.10-x86_64-minimal.iso",
            "--disk", f"path=/var/lib/libvirt/images/{vm_request.hostnamevm}.qcow2,size={str(vm_request.size)}",
            "--network", f"bridge={vm_request.tenant_name},virtualport_type=openvswitch",
            "--autostart",
            "--name", vm_request.hostnamevm,
            "--os-type", "linux",
            "--os-variant", "centos8",
            "--graphics=none",
            "--initrd-inject", ks_cfg_path,
            "--extra-args", f"console=ttyS0 inst.text inst.ks=file:/ks.cfg",
            "--noautoconsole"
        ]

        # Print the command for debugging purposes
        print(f"Running command: {' '.join(command)}")
        try:
            subprocess.run(command, check=True)
            print(f"Virtual machine {vm_request.hostnamevm} created successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual machine: {str(e)}")
            raise RuntimeError(f"Error creating virtual machine: {str(e)}")





class VirtInstallVMRemover(VMRemoverPort):
    def __init__(self, image_directory: str):
        self.image_directory = image_directory

    def remove(self, vm_id: int):
        # Connect to the local libvirt hypervisor
        conn = libvirt.open('qemu:///system')
        if conn is None:
            raise HTTPException(status_code=500, detail="Failed to connect to the hypervisor")

        try:
            # Check if the VM with the given ID is running
            if vm_id in conn.listDomainsID():
                # Get the domain (VM) object by ID
                domain = conn.lookupByID(vm_id)
                if domain is None:
                    raise HTTPException(status_code=404, detail=f"VM with ID {vm_id} not found")

                # Get the XML description of the VM
                xml_desc = domain.XMLDesc()
                # Find the path to the QCOW2 image file
                image_path = self.extract_image_path_from_xml(xml_desc)

                # Destroy (shut down) the domain (VM)
                domain.destroy()
                # Undefine (remove) the domain from the hypervisor
                domain.undefine()

                # Remove the QCOW2 image file
                if image_path:
                    full_image_path = os.path.join(self.image_directory, image_path)
                    if os.path.exists(full_image_path):
                        os.remove(full_image_path)
                    else:
                        raise HTTPException(status_code=404, detail=f"Image file not found at {full_image_path}")

                return {"status": "success", "detail": f"VM with ID {vm_id} and its image have been removed."}
            else:
                raise HTTPException(status_code=404, detail=f"No VM found with ID {vm_id}")
        finally:
            # Close the connection to the hypervisor
            conn.close()

    def extract_image_path_from_xml(self, xml_desc: str) -> str:
        # Example XML parsing to find the image path
        root = ET.fromstring(xml_desc)
        disk_element = root.find(".//disk[@device='disk']")
        if disk_element is not None:
            source_element = disk_element.find("source")
            if source_element is not None:
                return source_element.get("file")  # This should be relative path if `image_directory` is used
        return None








# src/adapters/out_process/virt/virt_adapter.py
class VirtInstallVMFetcher(VMFetcherPort):

    def __init__(self, image_directory: str):
        self.image_directory = image_directory

    def fetch(self, vm_id: int) -> VMDetailedInfo:
        conn = libvirt.open('qemu:///system')
        if conn is None:
            raise HTTPException(status_code=500, detail="Failed to connect to the hypervisor")

        try:
            if vm_id in conn.listDomainsID():
                domain = conn.lookupByID(vm_id)
                if domain is None:
                    raise HTTPException(status_code=404, detail=f"VM with ID {vm_id} not found")

                xml_desc = domain.XMLDesc()
                image_path = self.extract_image_path_from_xml(xml_desc)

                # Convert status code to string
                status = str(domain.info()[0])  # Convert status code to string

                return VMDetailedInfo(
                    id=vm_id,
                    name=domain.name(),
                    status=status,  # Ensure status is a string
                    memory=domain.info()[1],  # Memory in MB
                    vcpus=domain.info()[3],  # Number of VCPUs
                    disk_size=self.get_disk_size(image_path),
                    image_path=image_path
                )
            else:
                raise HTTPException(status_code=404, detail=f"No VM found with ID {vm_id}")
        finally:
            conn.close()




    def extract_image_path_from_xml(self, xml_desc: str) -> str:
            root = ET.fromstring(xml_desc)
            disk_element = root.find(".//disk[@device='disk']")
            if disk_element is not None:
                source_element = disk_element.find("source")
                if source_element is not None:
                    return source_element.get("file")  # This should be relative path if `image_directory` is used
            return None



    def get_disk_size(self, image_path: str) -> int:
            if image_path:
                full_image_path = os.path.join(self.image_directory, image_path)
                if os.path.exists(full_image_path):
                    return os.path.getsize(full_image_path)  # Size in bytes
            return 0
