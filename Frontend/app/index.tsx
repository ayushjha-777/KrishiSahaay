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

export default function HomeScreen() {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

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
        setImageUri(result.assets[0].uri);
      }
    } catch (error) {
      Alert.alert("Error", "Failed to select image.");
    }
  };

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

      const prediction =
        response.data.prediction;

      router.push({
        pathname: "/result",
        params: {
          image: imageUri,
          disease: prediction.prediction,
          confidence:
            prediction.confidence.toFixed(2),
        },
      });
    } catch (error: any) {
      console.log(error);

      Alert.alert(
        "Prediction Failed",
        "Unable to connect to the backend."
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
            <UploadCard onPress={pickImage} />
          ) : (
            <>
              <ImagePreview imageUri={imageUri} />

              <Text style={styles.changeImage}>
                Want to use another image?
              </Text>

              <Text
                style={styles.selectAgain}
                onPress={pickImage}
              >
                Select Another Image
              </Text>

              <AnalyzeButton
                loading={loading}
                onPress={analyzeImage}
              />
            </>
          )}

        </View>
      </ScrollView>
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
    marginTop: 18,
    textAlign: "center",
    color: COLORS.gray,
    fontSize: 15,
  },

  selectAgain: {
    textAlign: "center",
    color: COLORS.primary,
    fontWeight: "700",
    fontSize: 16,
    marginTop: 6,
    marginBottom: 10,
  },
});