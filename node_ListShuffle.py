import bpy
from node_s import *
from util import *
import random

class ListShuffleNode(Node, SverchCustomTreeNode):
    ''' List Shuffle Node '''
    bl_idname = 'ListShuffleNode'
    bl_label = 'List Shuffle'
    bl_icon = 'OUTLINER_OB_EMPTY'
    
    level = bpy.props.IntProperty(name = 'level_to_Shuffle', default=2, min=1, update=updateNode)
    seed = bpy.props.IntProperty(name = 'Seed', default=0, update=updateNode)
    
    typ = bpy.props.StringProperty(name='typ', default='')
    newsock = bpy.props.BoolProperty(name='newsock', default=False)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, 'level', text="level")
        layout.prop(self, 'seed',text="Seed")
    
    def init(self, context):
        self.inputs.new('StringsSocket', "data", "data")
        self.outputs.new('StringsSocket', 'data', 'data')
    
    def update(self):
        if 'data' in self.inputs and len(self.inputs['data'].links)>0:
            # адаптивный сокет
            inputsocketname = 'data'
            outputsocketname = ['data']
            changable_sockets(self, inputsocketname, outputsocketname)
        
        if 'data' in self.outputs and len(self.outputs['data'].links)>0:
            random.seed(self.seed)    
            data = SvGetSocketAnyType(self, self.inputs['data'])
            output = self.shuffle(data, self.level)
            SvSetSocketAnyType(self, 'data', output)

    def shuffle(self, lst, level):
        level -= 1
        if level:
            out = []
            for l in lst:
                out.append(self.shuffle(l, level))
            return out
        elif type(lst) in [type([])]:
            #print (type(list))
            random.shuffle(lst)
            return lst
        elif type(lst) in [type(tuple())]:
            lst = list(lst)
            random.shuffle(lst)
            return tuple(lst)

def register():
    bpy.utils.register_class(ListShuffleNode)
    
def unregister():
    bpy.utils.unregister_class(ListShuffleNode)

if __name__ == "__main__":
    register()