import { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { router } from "expo-router";

import Header from "../components/Header";
import UploadCard from "../components/UploadCard";
import ImagePreview from "../components/ImagePreview";
import AnalyzeButton from "../components/AnalyzeButton";

import api from "../services/api";
import { COLORS } from "../constants/colors";
import * as ImageManipulator from "expo-image-manipulator";
import LoadingOverlay from "../components/LoadingOverlay";
import { getErrorMessage } from "../utils/errors";
import { useFocusEffect } from "@react-navigation/native";
import { useCallback } from "react";

export default function HomeScreen() {
  useFocusEffect(
  useCallback(() => {
    setLoading(false);
    setImageUri(null);
    return () => {};
  }, [])
);
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  // -----------------------------
  // Gallery Picker
  // -----------------------------
  const pickImage = async () => {
  try {
    const permission =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permission.granted) {
      Alert.alert(
        "Permission Required",
        "Please allow gallery access."
      );
      return;
    }

    const result =
      await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 1,
      });

    if (!result.canceled) {

      const manipulated =
        await ImageManipulator.manipulateAsync(
          result.assets[0].uri,
          [
            {
              resize: {
                width: 512,
                height: 512,
              },
            },
          ],
          {
            compress: 0.8,
            format: ImageManipulator.SaveFormat.JPEG,
          }
        );

      setImageUri(manipulated.uri);
    }

  } catch {
    Alert.alert("Error", "Unable to open gallery.");
  }
};

  // -----------------------------
  // Camera
  // -----------------------------
  const takePhoto = async () => {
  try {
    const permission =
      await ImagePicker.requestCameraPermissionsAsync();

    if (!permission.granted) {
      Alert.alert(
        "Permission Required",
        "Please allow camera access."
      );
      return;
    }

    const result =
      await ImagePicker.launchCameraAsync({
        allowsEditing: true,
        aspect: [1, 1],
        quality: 1,
      });

    if (!result.canceled) {

      const manipulated =
        await ImageManipulator.manipulateAsync(
          result.assets[0].uri,
          [
            {
              resize: {
                width: 512,
                height: 512,
              },
            },
          ],
          {
            compress: 0.8,
            format: ImageManipulator.SaveFormat.JPEG,
          }
        );

      setImageUri(manipulated.uri);
    }

  } catch {
    Alert.alert("Error", "Unable to open camera.");
  }
};

  // -----------------------------
  // Analyze
  // -----------------------------
  const analyzeImage = async () => {
    if (!imageUri) {
      Alert.alert(
        "No Image Selected",
        "Please select a leaf image first."
      );
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("image", {
        uri: imageUri,
        name: "leaf.jpg",
        type: "image/jpeg",
      } as any);

      const response = await api.post(
        "/predict/",
        formData
      );

      const prediction = response.data.prediction;

      router.push({
        pathname: "/result",
        params: {
          image: imageUri,
          disease: prediction.prediction,
          confidence: prediction.confidence.toFixed(2),
        },
      });
    } catch (error: any) {
  console.log(error);

  const message =
    error?.response?.data?.message ||
    getErrorMessage(error);

  Alert.alert(
    "Invalid Image",
    message
  );
} finally {
  setLoading(false);
}
};

    return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scroll}
      >
        <Header />

        <View style={styles.content}>
          {!imageUri ? (
            <UploadCard
              onCameraPress={takePhoto}
              onGalleryPress={pickImage}
            />
          ) : (
            <>
              <ImagePreview imageUri={imageUri} />

              <Text style={styles.changeImage}>
                Want to analyze another leaf?
              </Text>

              <View style={styles.actionButtons}>
                <Text
                  style={styles.actionButton}
                  onPress={takePhoto}
                >
                  📷 Camera
                </Text>

                <Text
                  style={styles.actionButton}
                  onPress={pickImage}
                >
                  🖼 Gallery
                </Text>
              </View>

              <AnalyzeButton
                loading={loading}
                onPress={analyzeImage}
              />
            </>
          )}
        </View>
      </ScrollView>
      <LoadingOverlay visible={loading} />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },

  scroll: {
    paddingBottom: 40,
  },

  content: {
    paddingHorizontal: 20,
    marginTop: 15,
  },

  changeImage: {
    marginTop: 20,
    textAlign: "center",
    color: COLORS.gray,
    fontSize: 15,
    fontWeight: "500",
  },

  actionButtons: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 15,
    marginBottom: 15,
  },

  actionButton: {
    flex: 1,
    textAlign: "center",
    marginHorizontal: 6,
    paddingVertical: 14,
    backgroundColor: "#E8F5E9",
    borderRadius: 12,
    color: COLORS.primary,
    fontWeight: "700",
    fontSize: 16,
  },
});