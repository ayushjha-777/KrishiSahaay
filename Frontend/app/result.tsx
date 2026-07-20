import React from "react";
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../constants/colors";
import { formatDiseaseName } from "../utils/disease";

export default function ResultScreen() {
  const { disease, confidence, image, severityPercent, severityLevel } =
    useLocalSearchParams();

  const diseaseName = formatDiseaseName(String(disease));
  const hasSeverity = severityLevel && String(severityLevel).length > 0;

  const getDiseaseColor = () => {
    if (diseaseName === "Healthy") return COLORS.success;
    if (diseaseName === "Early Blight") return "#FB8C00";
    if (diseaseName === "Bacteria") return "#8E24AA";
    if (diseaseName === "Pest") return "#D84315";
    return COLORS.danger;
  };

  const getDiseaseIcon = () => {
    if (diseaseName === "Healthy") return "check-circle";
    if (diseaseName === "Early Blight") return "alert-circle";
    if (diseaseName === "Bacteria") return "bacteria-outline";
    if (diseaseName === "Pest") return "bug-outline";
    return "close-circle";
  };

  const getSeverityColor = () => {
    if (severityLevel === "Mild") return "#FBC02D";
    if (severityLevel === "Moderate") return "#FB8C00";
    return COLORS.danger;
  };

  return (
    <SafeAreaView style={styles.container}>

      <Text style={styles.title}>
        Analysis Result
      </Text>

      <View style={styles.imageCard}>
        <Image
          source={{ uri: String(image) }}
          style={styles.image}
        />
      </View>

      <View style={styles.resultCard}>

        <Text style={styles.label}>
          Disease Status
        </Text>

        <View style={styles.diseaseRow}>

          <MaterialCommunityIcons
            name={getDiseaseIcon()}
            size={28}
            color={getDiseaseColor()}
          />

          <Text
            style={[
              styles.disease,
              { color: getDiseaseColor() },
            ]}
          >
            {diseaseName}
          </Text>

        </View>

      </View>

      <View style={styles.confidenceCard}>

        <Text style={styles.label}>
          Confidence Score
        </Text>

        <Text style={styles.confidence}>
          {confidence}%
        </Text>

      </View>

      {hasSeverity && (
        <View style={styles.severityCard}>

          <Text style={styles.label}>
            Severity (Affected Leaf Area)
          </Text>

          <View style={styles.diseaseRow}>
            <MaterialCommunityIcons
              name="chart-donut"
              size={26}
              color={getSeverityColor()}
            />

            <Text
              style={[
                styles.severity,
                { color: getSeverityColor() },
              ]}
            >
              {severityLevel} ({severityPercent}%)
            </Text>
          </View>

          <View style={styles.severityBarTrack}>
            <View
              style={[
                styles.severityBarFill,
                {
                  width: `${Math.min(Number(severityPercent), 100)}%`,
                  backgroundColor: getSeverityColor(),
                },
              ]}
            />
          </View>

        </View>
      )}

      <TouchableOpacity
        style={styles.button}
        onPress={() => router.replace("/")}
      >
        <Text style={styles.buttonText}>
          Analyze Another Leaf
        </Text>
      </TouchableOpacity>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: 20,
  },

  title: {
    fontSize: 30,
    fontWeight: "700",
    color: COLORS.primary,
    textAlign: "center",
    marginVertical: 20,
  },

  imageCard: {
    backgroundColor: COLORS.white,
    borderRadius: 20,
    padding: 10,
    elevation: 5,
  },

  image: {
    width: "100%",
    height: 260,
    borderRadius: 15,
  },

  resultCard: {
    marginTop: 25,
    backgroundColor: COLORS.white,
    borderRadius: 20,
    padding: 20,
    elevation: 5,
  },

  confidenceCard: {
    marginTop: 20,
    backgroundColor: COLORS.white,
    borderRadius: 20,
    padding: 20,
    alignItems: "center",
    elevation: 5,
  },

  severityCard: {
    marginTop: 20,
    backgroundColor: COLORS.white,
    borderRadius: 20,
    padding: 20,
    elevation: 5,
  },

  severity: {
    fontSize: 22,
    fontWeight: "700",
    marginLeft: 10,
  },

  severityBarTrack: {
    marginTop: 14,
    height: 12,
    borderRadius: 6,
    backgroundColor: "#EEEEEE",
    overflow: "hidden",
  },

  severityBarFill: {
    height: "100%",
    borderRadius: 6,
  },

  label: {
    fontSize: 17,
    color: COLORS.gray,
    marginBottom: 10,
    fontWeight: "600",
  },

  diseaseRow: {
    flexDirection: "row",
    alignItems: "center",
  },

  disease: {
    fontSize: 28,
    fontWeight: "700",
    marginLeft: 10,
  },

  confidence: {
    fontSize: 42,
    color: COLORS.primary,
    fontWeight: "700",
  },

  button: {
    marginTop: "auto",
    backgroundColor: COLORS.primary,
    paddingVertical: 18,
    borderRadius: 18,
    alignItems: "center",
    marginBottom: 20,
  },

  buttonText: {
    color: "white",
    fontWeight: "700",
    fontSize: 18,
  },

});