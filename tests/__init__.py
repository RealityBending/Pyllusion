import pyllusion as ill
import numpy as np


def test_delbeouf():
    
    parameters1 = ill.delboeuf_parameters(illusion_strength=1, difference=-2, size_min=0.25)
    out1 = ill.delboeuf_image(parameters1)
    assert list(parameters1.keys()) == ['Difference', 'Size_Inner_Left', 'Size_Inner_Right',
                                        'Size_Inner_Difference', 'Illusion', 'Illusion_Strength',
                                        'Illusion_Type', 'Size_Outer_Left', 'Size_Outer_Right',
                                        'Distance_Centers', 'Distance_Edges_Inner', 'Distance_Edges_Outer',
                                        'Size_Inner_Smaller', 'Size_Inner_Larger', 'Size_Outer_Smaller',
                                        'Size_Outer_Larger', 'Position_Left', 'Position_Right']
    assert parameters1['Difference'] == -2
    assert parameters1['Illusion_Strength'] == 1
    assert parameters1['Illusion'] == 'Delboeuf'
    assert out1.size == (800, 600)

    parameters2 = ill.delboeuf_parameters(illusion_strength=1, difference=-2, size_min=0.5)
    out2 = ill.delboeuf_image(parameters2)  
    assert parameters1['Size_Inner_Smaller'] < parameters2['Size_Inner_Smaller'] 
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.delboeuf_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)
    
def test_ebbinghaus():
    
    parameters1 = ill.ebbinghaus_parameters(illusion_strength=2, difference=3, size_min=0.25)
    out1 = ill.ebbinghaus_image(parameters1)
    assert list(parameters1.keys()) == ['Difference', 'Size_Inner_Left', 'Size_Inner_Right',
                                        'Size_Inner_Difference', 'Illusion', 'Illusion_Strength',
                                        'Illusion_Type', 'Size_Outer_Left', 'Size_Outer_Right',
                                        'Distance_Centers', 'Distance_Edges_Inner', 'Distance_Edges_Outer',
                                        'Size_Inner_Smaller', 'Size_Inner_Larger', 'Size_Outer_Smaller',
                                        'Size_Outer_Larger', 'Position_Outer_x_Left',
                                        'Position_Outer_y_Left', 'Position_Outer_x_Right',
                                        'Position_Outer_y_Right', 'Position_Left', 'Position_Right']    
    assert parameters1['Difference'] == 3
    assert parameters1['Illusion_Strength'] == 2
    assert parameters1['Illusion'] == 'Ebbinghaus'
    assert out1.size == (800, 600)

    parameters2 = ill.ebbinghaus_parameters(illusion_strength=2, difference=3, size_min=0.5)
    out2 = ill.ebbinghaus_image(parameters2)  
    assert parameters1['Size_Inner_Smaller'] < parameters2['Size_Inner_Smaller'] 
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
                                        'Illusion', 'Illusion_Strength', 'Illusion_Type', 'Distractor_Length']
    assert parameters1['Difference'] == 0.3
    assert parameters1['Illusion_Strength'] == 30
    assert parameters1['Illusion'] == 'MullerLyer'
    assert out1.size == (800, 600)

    parameters2 = ill.mullerlyer_parameters(illusion_strength=30, difference=0.3, size_min=0.8)
    out2 = ill.mullerlyer_image(parameters2)  
    assert parameters1['Size_Smaller'] < parameters2['Size_Smaller'] 
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
    assert parameters1['Size_Bottom'] < parameters2['Size_Bottom'] 
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.ponzo_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)

def test_zollner():

    parameters1 = ill.zollner_parameters(illusion_strength=60, difference=0.5, distractors_n=5)
    out1 = ill.zollner_image(parameters1)
    assert list(parameters1.keys()) == ['Illusion', 'Illusion_Strength', 'Difference', 
                                        'Illusion_Type', 'Top_x1', 'Top_y1', 'Top_x2', 
                                        'Top_y2', 'Bottom_x1', 'Bottom_y1', 'Bottom_x2',
                                        'Bottom_y2', 'Distractors_n', 'Distractors_Top_x1',
                                        'Distractors_Top_y1', 'Distractors_Top_x2',
                                        'Distractors_Top_y2', 'Distractors_Bottom_x1', 
                                        'Distractors_Bottom_y1', 'Distractors_Bottom_x2', 
                                        'Distractors_Bottom_y2', 'Distractors_Angle']
    assert parameters1['Difference'] == 0.5
    assert parameters1['Illusion_Strength'] == 60
    assert parameters1['Illusion'] == 'Zollner'
    assert out1.size == (800, 600)

    parameters2 = ill.zollner_parameters(illusion_strength=60, difference=0.5, distractors_n=8)
    out2 = ill.zollner_image(parameters2)  
    assert parameters1['Distractors_n'] < parameters2['Distractors_n']
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.zollner_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)

def test_rodframe():

    parameters1 = ill.rodframe_parameters(illusion_strength=20, difference=10)
    out1 = ill.rodframe_image(parameters1)
    assert list(parameters1.keys()) == ['Illusion', 'Frame_Angle', 'Rod_Angle',
                                        'Angle_Difference',  'Difference',
                                        'Illusion_Strength', 'Illusion_Type']
    assert parameters1['Difference'] == 10
    assert parameters1['Illusion_Strength'] == 20
    assert parameters1['Illusion'] == 'RodFrame'
    assert out1.size == (800, 600)

    parameters2 = ill.rodframe_parameters(illusion_strength=20, difference=10)
    out2 = ill.rodframe_image(parameters2, outline=30)  
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.rodframe_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)


def test_verticalhorizontal():

    parameters1 = ill.verticalhorizontal_parameters(illusion_strength=90, difference=0)
    out1 = ill.verticalhorizontal_image(parameters1)
    assert list(parameters1.keys()) == ['Illusion', 'Size_Left', 'Size_Right',
                                        'Difference', 'Illusion_Strength', 'Illusion_Type',
                                        'Left_x1', 'Left_y1', 'Left_x2', 'Left_y2', 
                                        'Left_Angle', 'Right_x1', 'Right_y1', 
                                        'Right_x2', 'Right_y2', 'Right_Angle']
    assert parameters1['Difference'] == 0
    assert parameters1['Illusion_Strength'] == 90
    assert parameters1['Illusion'] == 'VerticalHorizontal'
    assert out1.size == (800, 600)

    parameters2 = ill.verticalhorizontal_parameters(illusion_strength=90, difference=0.5)
    out2 = ill.verticalhorizontal_image(parameters2)  
    assert parameters1['Difference'] < parameters2['Difference']
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.verticalhorizontal_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)


def test_poggendorff():

    parameters1 = ill.poggendorff_parameters(illusion_strength=40, difference=0)
    out1 = ill.poggendorff_image(parameters1)
    assert list(parameters1.keys()) == ['Illusion', 'Illusion_Strength', 'Difference',
                                        'Illusion_Type', 'Left_x1', 'Left_y1', 'Left_x2', 
                                        'Left_y2', 'Right_x1', 'Right_y1', 'Right_x2', 
                                        'Right_y2', 'Angle', 'Rectangle_Height',
                                        'Rectangle_Width', 'Rectangle_y']
    assert parameters1['Difference'] == 0
    assert parameters1['Illusion_Strength'] == 40
    assert parameters1['Illusion'] == 'Poggendorff'
    assert out1.size == (800, 600)

    parameters2 = ill.poggendorff_parameters(illusion_strength=40, difference=0.3)
    out2 = ill.poggendorff_image(parameters2)  
    assert parameters1['Difference'] < parameters2['Difference']
    assert np.mean(np.array(out1)) == np.mean(np.array(out2))

    out3 = ill.verticalhorizontal_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)


def test_contrast():

    parameters1 = ill.contrast_parameters(illusion_strength=-50, difference=10)
    out1 = ill.contrast_image(parameters1)
    assert list(parameters1.keys()) == ['Illusion', 'Illusion_Strength', 'Difference', 
                                        'Illusion_Type', 'Rectangle_Top', 'Rectangle_Bottom',
                                        'Background_Top', 'Background_Bottom', 'Rectangle_Top_RGB',
                                        'Rectangle_Bottom_RGB', 'Background_Top_RGB',
                                        'Background_Bottom_RGB']
    assert parameters1['Difference'] == 10
    assert parameters1['Illusion_Strength'] == -50
    assert parameters1['Illusion'] == 'Contrast'
    assert out1.size == (800, 600)

    parameters2 = ill.contrast_parameters(illusion_strength=0, difference=0)
    out2 = ill.contrast_image(parameters2)
    assert parameters1['Difference'] > parameters2['Difference']
    assert parameters1['Illusion_Strength'] < parameters2['Illusion_Strength']
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ill.contrast_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)


def test_white():
    
    parameters1 = ill.white_parameters(illusion_strength=100, difference=0)
    out1 = ill.white_image(parameters1)
    assert list(parameters1.keys()) == ['Illusion', 'Illusion_Strength', 'Difference',
                                        'Illusion_Type', 'Target1', 'Target2', 
                                        'Background1', 'Background2', 'Target1_RGB', 
                                        'Target2_RGB', 'Background1_RGB', 'Background2_RGB',
                                        'Target1_y', 'Target2_y', 'Target_Height']
    assert parameters1['Difference'] == 0
    assert parameters1['Illusion_Strength'] == 100
    assert parameters1['Illusion'] == 'Contrast'
    assert out1.size == (800, 600)

    parameters2 = ill.white_parameters(illusion_strength=100, difference=60)
    out2 = ill.white_image(parameters2)  
    assert parameters1['Difference'] < parameters2['Difference']
    assert np.mean(np.array(out1)) < np.mean(np.array(out2))

    out3 = ill.white_image(parameters2, width=900, height=900)  
    assert out3.size == (900, 900)
