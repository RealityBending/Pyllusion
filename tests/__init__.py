import pyllusion as ill
import PIL.Image
import numpy as np


def test_delbeouf():
    
    parameters1 = ill.delboeuf_parameters(illusion_strength=1, difference=-2, size_min=0.25)
    out1 = ill.delboeuf_image(parameters1)
    assert list(parameters1.keys()) == ['Difference',
                                        'Size_Inner_Left',
                                        'Size_Inner_Right',
                                        'Size_Inner_Difference',
                                        'Illusion',
                                        'Illusion_Strength',
                                        'Illusion_Type',
                                        'Size_Outer_Left',
                                        'Size_Outer_Right',
                                        'Distance_Centers',
                                        'Distance_Edges_Inner',
                                        'Distance_Edges_Outer',
                                        'Size_Inner_Smaller',
                                        'Size_Inner_Larger',
                                        'Size_Outer_Smaller',
                                        'Size_Outer_Larger',
                                        'Position_Left',
                                        'Position_Right']
    assert parameters1['Difference'] == -2
    assert parameters1['Illusion_Strength'] == 1
    assert parameters1['Ilusion'] == 'Delboeuf'
    assert out1.size == (800, 600)

    parameters2 = ill.delboeuf_parameters(illusion_strength=1, difference=-2, size_min=0.5)
    out2 = ill.delboeuf_image(parameters2)  
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.delboeuf_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)
    
def test_ebbinghaus():
    
    parameters1 = ill.ebbinghaus_parameters(illusion_strength=2, difference=3, size_min=0.25)
    out1 = ill.ebbinghaus_image(parameters1)
    assert list(parameters1.keys()) == ['Difference',
                                        'Size_Inner_Left',
                                        'Size_Inner_Right',
                                        'Size_Inner_Difference',
                                        'Illusion',
                                        'Illusion_Strength',
                                        'Illusion_Type',
                                        'Size_Outer_Left',
                                        'Size_Outer_Right',
                                        'Distance_Centers',
                                        'Distance_Edges_Inner',
                                        'Distance_Edges_Outer',
                                        'Size_Inner_Smaller',
                                        'Size_Inner_Larger',
                                        'Size_Outer_Smaller',
                                        'Size_Outer_Larger',
                                        'Position_Outer_x_Left',
                                        'Position_Outer_y_Left',
                                        'Position_Outer_x_Right',
                                        'Position_Outer_y_Right',
                                        'Position_Left',
                                        'Position_Right']    
    assert parameters1['Difference'] == 3
    assert parameters1['Illusion_Strength'] == 2
    assert parameters1['Illusion'] == 'Ebbinghaus'
    assert out1.size == (800, 600)

    parameters2 = ill.ebbinghaus_parameters(illusion_strength=2, difference=3, size_min=0.5)
    out2 = ill.ebbinghaus_image(parameters2)  
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.ebbinghaus_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)


