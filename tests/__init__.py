import pyllusion
import numpy as np


def test_delbeouf():

    delboeuf1 = pyllusion.Delboeuf(illusion_strength=1, difference=-2, size_min=0.25)
    out1 = delboeuf1.to_image()
    parameters1 = delboeuf1.get_parameters()
    assert list(parameters1) == ['Difference', 'Size_Inner_Left', 'Size_Inner_Right', 
                                 'Size_Inner_Difference', 'Illusion', 'Illusion_Strength',
                                 'Illusion_Type', 'Size_Outer_Left', 'Size_Outer_Right',
                                 'Distance', 'Distance_Reference', 'Distance_Edges_Inner',
                                 'Distance_Edges_Outer', 'Size_Inner_Smaller',
                                 'Size_Inner_Larger', 'Size_Outer_Smaller',
                                 'Size_Outer_Larger', 'Position_Left', 'Position_Right']
    assert parameters1['Difference'] == -2
    assert parameters1['Illusion_Strength'] == 1
    assert parameters1['Illusion'] == 'Delboeuf'
    assert out1.size == (800, 600)

    delboeuf2 = pyllusion.Delboeuf(illusion_strength=1, difference=-2, size_min=0.5)
    out2 = delboeuf2.to_image()
    parameters2 = delboeuf2.get_parameters()
    assert parameters1['Size_Inner_Smaller'] < parameters2['Size_Inner_Smaller'] 
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = delboeuf2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_ebbinghaus():
    
    ebbinghaus1 = pyllusion.Ebbinghaus(illusion_strength=2, difference=3, size_min=0.25)
    out1 = ebbinghaus1.to_image()
    parameters1 = ebbinghaus1.get_parameters()
    assert list(parameters1) == ['Difference', 'Size_Inner_Left', 'Size_Inner_Right',
                                 'Size_Inner_Difference', 'Illusion', 'Illusion_Strength',
                                 'Illusion_Type', 'Size_Outer_Left', 'Size_Outer_Right',
                                 'Distance', 'Distance_Reference', 'Distance_Edges_Inner',        
                                 'Distance_Edges_Outer',
                                 'Size_Inner_Smaller', 'Size_Inner_Larger', 'Size_Outer_Smaller',
                                 'Size_Outer_Larger', 'Position_Outer_x_Left',
                                 'Position_Outer_y_Left', 'Position_Outer_x_Right',
                                 'Position_Outer_y_Right', 'Position_Left', 'Position_Right']    
    assert parameters1['Difference'] == 3
    assert parameters1['Illusion_Strength'] == 2
    assert parameters1['Illusion'] == 'Ebbinghaus'
    assert out1.size == (800, 600)

    ebbinghaus2 = pyllusion.Ebbinghaus(illusion_strength=2, difference=3, size_min=0.5)
    out2 = ebbinghaus2.to_image()
    parameters2 = ebbinghaus2.get_parameters()
    assert parameters1['Size_Inner_Smaller'] < parameters2['Size_Inner_Smaller'] 
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ebbinghaus2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_mullerlyer():
    
    mullerlyer1 = pyllusion.MullerLyer(illusion_strength=30, difference=0.3, size_min=0.5)
    out1 = mullerlyer1.to_image()
    parameters1 = mullerlyer1.get_parameters()
    assert list(parameters1) == ['Difference', 'Distance', 'Bottom_x1',
                                 'Bottom_y1', 'Bottom_x2', 'Bottom_y2',
                                 'Top_x1', 'Top_y1','Top_x2', 'Top_y2', 'Size_Bottom',
                                 'Size_Top', 'Size_Larger', 'Size_Smaller', 'Distractor_TopLeft1_x1',
                                 'Distractor_TopLeft1_y1', 'Distractor_TopLeft1_x2',
                                 'Distractor_TopLeft1_y2',
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

    mullerlyer2 = pyllusion.MullerLyer(illusion_strength=30, difference=0.3, size_min=0.8)
    out2 = mullerlyer2.to_image()  
    parameters2 = mullerlyer2.get_parameters()
    assert parameters1['Size_Smaller'] < parameters2['Size_Smaller'] 
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = mullerlyer2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_ponzo():

    ponzo1 = pyllusion.Ponzo(illusion_strength=20, difference=0.2, size_min=0.5)
    out1 = ponzo1.to_image()
    parameters1 = ponzo1.get_parameters()
    assert list(parameters1) == ['Difference', 'Distance', 'Bottom_x1', 'Bottom_y1',
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

    ponzo2 = pyllusion.Ponzo(illusion_strength=20, difference=0.2, size_min=0.8)
    out2 = ponzo2.to_image()
    parameters2 = ponzo2.get_parameters()
    assert parameters1['Size_Bottom'] < parameters2['Size_Bottom'] 
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = ponzo2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_zollner():

    zollner1 = pyllusion.Zollner(illusion_strength=60, difference=0.5, distractors_n=5)
    out1 = zollner1.to_image()
    parameters1 = zollner1.get_parameters()
    assert list(parameters1) == ['Illusion', 'Illusion_Strength', 'Difference', 
                                 'Illusion_Type', 'Top_x1', 'Top_y1', 'Top_x2', 
                                 'Top_y2', 'Bottom_x1', 'Bottom_y1', 'Bottom_x2',
                                 'Bottom_y2', 'Distractors_n', 'Distractors_Size', 'Distractors_Top_x1',
                                 'Distractors_Top_y1', 'Distractors_Top_x2',
                                 'Distractors_Top_y2', 'Distractors_Bottom_x1', 
                                 'Distractors_Bottom_y1', 'Distractors_Bottom_x2', 
                                 'Distractors_Bottom_y2', 'Distractors_Angle']
    assert parameters1['Difference'] == 0.5
    assert parameters1['Illusion_Strength'] == 60
    assert parameters1['Illusion'] == 'Zollner'
    assert out1.size == (800, 600)

    zollner2 = pyllusion.Zollner(illusion_strength=60, difference=0.5, distractors_n=8)
    out2 = zollner2.to_image()  
    parameters2 = zollner2.get_parameters()
    assert parameters1['Distractors_n'] < parameters2['Distractors_n']
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = zollner2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_rodframe():

    rodframe1 = pyllusion.RodFrame(illusion_strength=20, difference=10)
    out1 = rodframe1.to_image()
    parameters1 = rodframe1.get_parameters()
    assert list(parameters1) == ['Illusion', 'Frame_Angle', 'Rod_Angle',
                                 'Angle_Difference',  'Difference',
                                 'Illusion_Strength', 'Illusion_Type']
    assert parameters1['Difference'] == 10
    assert parameters1['Illusion_Strength'] == 20
    assert parameters1['Illusion'] == 'RodFrame'
    assert out1.size == (800, 600)

    rodframe2 = pyllusion.RodFrame(illusion_strength=20, difference=10)
    out2 = rodframe2.to_image(outline=30)  
    parameters2 = rodframe2.get_parameters()
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = rodframe2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_verticalhorizontal():

    verticalhorizontal1 = pyllusion.VerticalHorizontal(illusion_strength=90, difference=0)
    out1 = verticalhorizontal1.to_image()
    parameters1 = verticalhorizontal1.get_parameters()
    assert list(parameters1) == ['Illusion', 'Size_Left', 'Size_Right',
                                 'Size_Larger', 'Size_Smaller',
                                 'Difference', 'Illusion_Strength', 'Illusion_Type',
                                 'Left_x1', 'Left_y1', 'Left_x2', 'Left_y2', 
                                 'Left_Angle', 'Right_x1', 'Right_y1', 
                                 'Right_x2', 'Right_y2', 'Right_Angle']
    assert parameters1['Difference'] == 0
    assert parameters1['Illusion_Strength'] == 90
    assert parameters1['Illusion'] == 'VerticalHorizontal'
    assert out1.size == (800, 600)

    verticalhorizontal2 = pyllusion.VerticalHorizontal(illusion_strength=90, difference=0.5)
    out2 = verticalhorizontal2.to_image()  
    parameters2 = verticalhorizontal2.get_parameters()
    assert parameters1['Difference'] < parameters2['Difference']
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = verticalhorizontal2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_poggendorff():

    poggendorff1 = pyllusion.Poggendorff(illusion_strength=40, difference=0)
    out1 = poggendorff1.to_image()
    parameters1 = poggendorff1.get_parameters()
    assert list(parameters1) == ['Illusion', 'Illusion_Strength', 'Difference',
                                 'Illusion_Type', 'Left_x1', 'Left_y1', 'Left_x2', 
                                 'Left_y2', 'Right_x1', 'Right_y1', 'Right_x2', 
                                 'Right_y2', 'Angle', 'Rectangle_Height',
                                 'Rectangle_Width']
    assert parameters1['Difference'] == 0
    assert parameters1['Illusion_Strength'] == 40
    assert parameters1['Illusion'] == 'Poggendorff'
    assert out1.size == (800, 600)

    poggendorff2 = pyllusion.Poggendorff(illusion_strength=40, difference=0.3)
    out2 = poggendorff2.to_image()  
    parameters2 = poggendorff2.get_parameters()
    assert parameters1['Difference'] < parameters2['Difference']
    assert np.mean(np.array(out1)) == np.mean(np.array(out2))

    out3 = poggendorff2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_contrast():

    contrast1 = pyllusion.Contrast(illusion_strength=-50, difference=10)
    out1 = contrast1.to_image()
    parameters1 = contrast1.get_parameters()
    assert list(parameters1) == ['Illusion', 'Illusion_Strength', 'Difference', 
                                 'Illusion_Type', 'Rectangle_Top', 'Rectangle_Bottom',
                                 'Background_Top', 'Background_Bottom', 'Rectangle_Top_RGB',
                                 'Rectangle_Bottom_RGB', 'Background_Top_RGB',
                                 'Background_Bottom_RGB']
    assert parameters1['Difference'] == 10
    assert parameters1['Illusion_Strength'] == -50
    assert parameters1['Illusion'] == 'Contrast'
    assert out1.size == (800, 600)

    contrast2 = pyllusion.Contrast(illusion_strength=0, difference=0)
    out2 = contrast2.to_image()
    parameters2 = contrast2.get_parameters()
    assert parameters1['Difference'] > parameters2['Difference']
    assert parameters1['Illusion_Strength'] < parameters2['Illusion_Strength']
    assert np.mean(np.array(out1)) > np.mean(np.array(out2))

    out3 = contrast2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)

def test_white():
    
    white1 = pyllusion.White(illusion_strength=100, difference=0)
    out1 = white1.to_image()
    parameters1 = white1.get_parameters() 
    assert list(parameters1) == ['Illusion', 'Illusion_Strength', 'Difference',
                                 'Illusion_Type', 'Target1', 'Target2', 
                                 'Background1', 'Background2', 'Target1_RGB', 
                                 'Target2_RGB', 'Background1_RGB', 'Background2_RGB',
                                 'Target1_y', 'Target2_y', 'Target_Height',
                                 'Target_n']
    assert parameters1['Difference'] == 0
    assert parameters1['Illusion_Strength'] == 100
    assert parameters1['Illusion'] == "White's"
    assert out1.size == (800, 600)

    white2 = pyllusion.White(illusion_strength=100, difference=60)
    out2 = white2.to_image()  
    parameters2 = white2.get_parameters()
    assert parameters1['Difference'] < parameters2['Difference']
    assert np.mean(np.array(out1)) < np.mean(np.array(out2))

    out3 = white2.to_image(width=900, height=900)  
    assert out3.size == (900, 900)
