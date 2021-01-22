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

def test_mullerlyer():
    
    parameters1 = ill.mullerlyer_parameters(illusion_strength=30, difference=0.3, size_min=0.5)
    out1 = ill.mullerlyer_image(parameters1)
    assert list(parameters1.keys()) == ['Difference', 'Distance', 'Bottom_x1',
                                        'Bottom_y1', 'Bottom_x2', 'Bottom_y2',
                                        'Top_x1', 'Top_y1','Top_x2', 'Top_y2', 'Size_Bottom',
                                        'Size_Top', 'Size_Larger', 'Size_Smaller', 'Distractor_TopLeft1_x1',
                                        'Distractor_TopLeft1_y1', 'Distractor_TopLeft1_x2', 'Distractor_TopLeft1_y2',
                                        'Distractor_TopLeft2_x1', 'Distractor_TopLeft2_y1', 
                                        'Distractor_TopLeft2_x2', 'Distractor_TopLeft2_y2',
                                        'Distractor_TopRight1_x1', 'Distractor_TopRight1_y1', 
                                        'Distractor_TopRight1_x2', 'Distractor_TopRight1_y2', 
                                        'Distractor_TopRight2_x1', 'Distractor_TopRight2_y1', 
                                        'Distractor_TopRight2_x2', 'Distractor_TopRight2_y2',
                                        'Distractor_BottomLeft1_x1', 'Distractor_BottomLeft1_y1',
                                        'Distractor_BottomLeft1_x2', 'Distractor_BottomLeft1_y2', 
                                        'Distractor_BottomLeft2_x1', 'Distractor_BottomLeft2_y1', 
                                        'Distractor_BottomLeft2_x2', 'Distractor_BottomLeft2_y2', 
                                        'Distractor_BottomRight1_x1', 'Distractor_BottomRight1_y1', 
                                        'Distractor_BottomRight1_x2', 'Distractor_BottomRight1_y2',
                                        'Distractor_BottomRight2_x1', 'Distractor_BottomRight2_y1',
                                        'Distractor_BottomRight2_x2', 'Distractor_BottomRight2_y2', 
                                        'Illusion', 'Illusion_Type', 'Distractor_Length']
    assert parameters1['Difference'] == 0.3
    assert parameters1['Illusion_Strength'] == 30
    assert parameters1['Illusion'] == 'MullerLyer'
    assert out1.size == (800, 600)

    parameters2 = ill.mullerlyer_parameters(illusion_strength=30, difference=0.3, size_min=0.8)
    out2 = ill.mullerlyer_image(parameters2)  
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.mullerlyer_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)

def test_ponzo():

    parameters1 = ill.ponzo_parameters(illusion_strength=20, difference=0.2, size_min=0.5)
    out1 = ill.ponzo_image(parameters1)
    assert list(parameters1.keys()) == ['Difference', 'Distance', 'Bottom_x1', 'Bottom_y1',
                                        'Bottom_x2', 'Bottom_y2', 'Top_x1', 'Top_y1',
                                        'Top_x2', 'Top_y2', 'Size_Bottom', 'Size_Top',
                                        'Size_Larger', 'Size_Smaller', 'Illusion_Strength',
                                        'Illusion_Type', 'Side_Angle', 'Side_Length',
                                        'Left_x1', 'Left_y1', 'Left_x2', 'Left_y2', 
                                        'Right_x1', 'Right_y1', 'Right_x2', 'Right_y2', 'Illusion']
    assert parameters1['Difference'] == 0.2
    assert parameters1['Illusion_Strength'] == 20
    assert parameters1['Illusion'] == 'Ponzo'
    assert out1.size == (800, 600)

    parameters2 = ill.ponzo_parameters(illusion_strength=20, difference=0.2, size_min=0.8)
    out2 = ill.ponzo_image(parameters2)  
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.ponzo_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)
    