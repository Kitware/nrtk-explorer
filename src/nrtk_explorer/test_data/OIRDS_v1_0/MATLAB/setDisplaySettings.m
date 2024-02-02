function setDisplaySettings(image)
    
    imSize = getImageSize(image);

    axis('equal');
    axis('off');
    set(gcf, 'Toolbar', 'none');
    set(gcf, 'Color', [0,0,0]);
    set(gcf, 'Resize', 'off');
    set(gcf, 'OuterPosition', [0,0,1600,1200]);
    
    set(gca, 'Units', 'pixels');
    position = get(gcf, 'Position');
    
    axisCenterX = position(1) + (position(3) / 2);
    axisCenterY = position(2) + (position(4) / 2);
    
    axisPosition = [axisCenterX - imSize(1), axisCenterY - imSize(2), imSize(1) * 2, imSize(2) * 2];
    
    set(gca, 'Position', axisPosition);

end