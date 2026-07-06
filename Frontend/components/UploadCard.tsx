import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../constants/colors";

interface UploadCardProps {
  onCameraPress: () => void;
  onGalleryPress: () => void;
}

export default function UploadCard({
  onCameraPress,
  onGalleryPress,
}: UploadCardProps) {
  return (
    <View style={styles.card}>
      <View style={styles.iconContainer}>
        <MaterialCommunityIcons
          name="leaf"
          size={48}
          color={COLORS.primary}
        />
      </View>

      <Text style={styles.title}>Upload Potato Leaf</Text>

      <Text style={styles.subtitle}>
        Capture a new photo or choose one from your gallery to analyze.
      </Text>

      <TouchableOpacity
        style={[styles.button, styles.cameraButton]}
        onPress={onCameraPress}
      >
        <MaterialCommunityIcons
          name="camera"
          size={22}
          color="white"
        />

        <Text style={styles.buttonText}>
          Take Photo
        </Text>
      </TouchableOpacity>

      <Text style={styles.orText}>OR</Text>

      <TouchableOpacity
        style={[styles.button, styles.galleryButton]}
        onPress={onGalleryPress}
      >
        <MaterialCommunityIcons
          name="image"
          size={22}
          color={COLORS.primary}
        />

        <Text style={styles.galleryText}>
          Choose from Gallery
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.white,
    marginHorizontal: 20,
    marginTop: 25,
    borderRadius: 20,
    padding: 25,
    elevation: 5,
    alignItems: "center",
  },

  iconContainer: {
    width: 85,
    height: 85,
    borderRadius: 45,
    backgroundColor: "#E8F5E9",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 18,
  },

  title: {
    fontSize: 22,
    fontWeight: "700",
    color: COLORS.primary,
    marginBottom: 8,
  },

  subtitle: {
    textAlign: "center",
    color: COLORS.gray,
    fontSize: 15,
    lineHeight: 22,
    marginBottom: 25,
  },

  button: {
    width: "100%",
    height: 55,
    borderRadius: 14,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
  },

  cameraButton: {
    backgroundColor: COLORS.primary,
  },

  galleryButton: {
    borderWidth: 2,
    borderColor: COLORS.primary,
    backgroundColor: "white",
  },

  buttonText: {
    color: "white",
    fontSize: 17,
    fontWeight: "700",
    marginLeft: 10,
  },

  galleryText: {
    color: COLORS.primary,
    fontSize: 17,
    fontWeight: "700",
    marginLeft: 10,
  },

  orText: {
    marginVertical: 15,
    color: COLORS.gray,
    fontWeight: "700",
  },
});