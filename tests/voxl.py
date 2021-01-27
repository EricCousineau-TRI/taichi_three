import taichi as ti
import numpy as np
import tina

ti.init(ti.gpu)

dens = np.load('assets/smoke.npy')[::1, ::1, ::1]
scene = tina.PTScene()
scene.engine.skybox = tina.Atomsphere()
volume = tina.SimpleVolume(N=dens.shape[0])
scene.add_object(tina.MeshModel('assets/monkey.obj'))
#scene.add_object(volume, tina.VolLambert())# * [0.8, 0.9, 0.8])
g = tina.Param(float, initial=0.76)
scene.add_object(volume, tina.HenyeyGreenstein(g=g))

gui = ti.GUI('volume', scene.res)
g.make_slider(gui, 'g', -1, 1, 0.01)

volume.set_volume_density(dens)
scene.update()
while gui.running:
    scene.input(gui)
    scene.render()#nsteps=32)
    gui.set_image(scene.img)
    gui.show()
