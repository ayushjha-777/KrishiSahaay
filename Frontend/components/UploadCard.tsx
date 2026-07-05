import React from "react";
import { TouchableOpacity, Text, StyleSheet, View } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../constants/colors";

interface UploadCardProps {
  onPress: () => void;
}

export default function UploadCard({ onPress }: UploadCardProps) {
  return (
    <TouchableOpacity style={styles.card} onPress={onPress}>
      <View style={styles.iconContainer}>
        <MaterialCommunityIcons
          name="image-plus"
          size={45}
          color={COLORS.primary}
        />
      </View>

      <Text style={styles.title}>Upload Leaf Image</Text>

      <Text style={styles.subtitle}>
        Tap here to select an image from your gallery
      </Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.white,
    marginHorizontal: 20,
    marginTop: 25,
    borderRadius: 20,
    borderWidth: 2,
    borderStyle: "dashed",
    borderColor: "#A5D6A7",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 35,
    paddingHorizontal: 20,
    elevation: 4,
  },

  iconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: "#E8F5E9",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 18,
  },

  title: {
    fontSize: 20,
    fontWeight: "700",
    color: COLORS.primary,
    marginBottom: 8,
  },

  subtitle: {
    textAlign: "center",
    color: COLORS.gray,
    fontSize: 14,
    lineHeight: 20,
  },
});