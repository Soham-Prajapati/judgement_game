import React from 'react';
import { Image, StyleSheet, TouchableOpacity, View } from 'react-native';
import { CardAssets } from '../core/assets';
import { Card } from '../models/card';

interface CardViewProps {
  card?: Card;
  back?: boolean;
  onPress?: () => void;
  disabled?: boolean;
  style?: any;
  size?: 'small' | 'medium' | 'large';
}

const CardView: React.FC<CardViewProps> = ({ card, back, onPress, disabled, style, size = 'medium' }) => {
  const assetKey = back ? 'back1' : `${card?.suit}${card?.rank}`;
  const source = CardAssets[assetKey];

  const dimensions = {
    small: { width: 50, height: 70 },
    medium: { width: 70, height: 100 },
    large: { width: 90, height: 130 },
  }[size];

  if (!source) {
    return <View style={[styles.placeholder, dimensions, style]} />;
  }

  const content = (
    <Image 
      source={source} 
      style={[dimensions, style]} 
      resizeMode="contain"
    />
  );

  if (onPress) {
    return (
      <TouchableOpacity onPress={onPress} disabled={disabled} activeOpacity={0.7}>
        {content}
      </TouchableOpacity>
    );
  }

  return content;
};

const styles = StyleSheet.create({
  placeholder: {
    backgroundColor: '#ccc',
    borderRadius: 8,
  },
});

export default CardView;
