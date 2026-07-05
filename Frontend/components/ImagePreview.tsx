import React from "react";
import { View, Image, Text, StyleSheet } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../constants/colors";

interface ImagePreviewProps {
  imageUri: string;
}

export default function ImagePreview({
  imageUri,
}: ImagePreviewProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Selected Image</Text>

      <Image
        source={{ uri: imageUri }}
        style={styles.image}
        resizeMode="cover"
      />

      <View style={styles.footer}>
        <MaterialCommunityIcons
          name="check-circle"
          size={18}
          color={COLORS.success}
        />

        <Text style={styles.footerText}>
          Image ready for analysis
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginHorizontal: 20,
    marginTop: 25,
    backgroundColor: COLORS.white,
    borderRadius: 20,
    padding: 15,
    elevation: 4,
  },

  heading: {
    fontSize: 18,
    fontWeight: "700",
    color: COLORS.text,
    marginBottom: 12,
  },

  image: {
    width: "100%",
    height: 250,
    borderRadius: 16,
  },

  footer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 12,
  },

  footerText: {
    marginLeft: 8,
    color: COLORS.success,
    fontWeight: "600",
  },
});