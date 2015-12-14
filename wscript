import shutil, re
from waflib import TaskGen
from waflib.Task import Task

class nvcompress(Task):
    color = 'PINK'
    def keyword(self):
        return "NVCompressing"
    def run(self):
        return self.exec_command('%s %s "%s" "%s" > /dev/null' % (
            self.env.NVCOMPRESS[0],
            self.__dict__['compression'],
            self.inputs[0].abspath(),
            self.outputs[0].abspath()))

@TaskGen.extension('nmap.png', 'nmap.jpg', 'nmap.jpeg')
def process(self, node):
    self.create_task('nvcompress', node, node.change_ext('.dds'), compression='-bc5 -normal')

@TaskGen.extension('.png', '.jpg', '.jpeg')
def process(self, node):
    self.create_task('nvcompress', node, node.change_ext('.dds'), compression='-bc3')

class mtl(Task):
    color = 'BLUE'
    def keyword(self):
        return "Processing"
    def run(self):
        with open(self.inputs[0].abspath()) as inp, open(self.outputs[0].abspath(), "w") as out:
            for line in inp:
                out.write(re.sub(r'\.(png|jpe?g)', '.dds', line))

@TaskGen.extension('.mtl', '.3ds')
def process(self, node):
    self.create_task('mtl', node, node.get_bld())

class copy(Task):
    color = 'BLUE'
    def keyword(self):
        return "Copying"
    def run(self):
        shutil.copy(self.inputs[0].abspath(), self.outputs[0].abspath())

@TaskGen.feature('copy')
def process(self):
    self.create_task('copy', self.source[0], self.source[0].get_bld())

def options(opt):
    pass

def configure(cnf):
    cnf.find_program('nvcompress')

def build(bld):
    bld(source=bld.path.ant_glob(['**/*.png', '**/*.jpg', '**/*.jpeg']))
    bld(source=bld.path.ant_glob('**/*.mtl'))
    bld(features='copy', source=bld.path.ant_glob('**/*.obj'))
