import subprocess

def run_cmd(cmd, input=""):
    subp = subprocess.Popen(cmd, shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    stdout, stderr = subp.communicate(input)
    if stderr:
        print(stderr)
    return stdout

def assemble(input_filename, output_filename):
    # Assemble the assembly using nasm
    # nasm -f elf new.asm -o
    pipe = "nasm -f elf {file} -o {output}".format(
        file=input_filename,
        output=output_filename,
    )
    run_cmd(pipe)
    pass


def load_shellcode(filename):
    # read shellcode from a compiled object file
    pipe = """objdump -d {} | tr '\t' ' ' | tr ' ' '\n' | egrep '^[0-9a-f]{{2}}$' | paste -d '' -s""".format(
        filename
    )
    return run_cmd(pipe).strip().decode('hex')
