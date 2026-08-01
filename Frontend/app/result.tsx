import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
} from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../constants/colors";
import { formatDiseaseName } from "../utils/disease";

export default function ResultScreen() {
  const {
    disease,
    confidence,
    image,
    severityPercent,
    severityLevel,
    lesionArea,
    lesionCount,
    avgLesionSize,
    colorScore,
    distributionScore,
  } = useLocalSearchParams();

  const [showAnalysis, setShowAnalysis] = useState(false);

  const diseaseName = formatDiseaseName(String(disease));

  const hasSeverity =
    severityLevel &&
    String(severityLevel).length > 0;

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

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >

        {/* TITLE */}
        <Text style={styles.title}>
          Analysis Result
        </Text>


        {/* IMAGE */}
        <View style={styles.imageCard}>
          <Image
            source={{ uri: String(image) }}
            style={styles.image}
          />
        </View>


        {/* DISEASE RESULT */}
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


        {/* CONFIDENCE */}
        <View style={styles.confidenceCard}>

          <Text style={styles.label}>
            Confidence Score
          </Text>

          <Text style={styles.confidence}>
            {confidence}%
          </Text>

        </View>


        {/* SEVERITY */}
        {hasSeverity && (

          <View style={styles.severityCard}>

            <Text style={styles.label}>
              Disease Severity
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


            {/* SEVERITY BAR */}
            <View style={styles.severityBarTrack}>

              <View
                style={[
                  styles.severityBarFill,
                  {
                    width: `${Math.min(
                      Math.max(Number(severityPercent) || 0, 0),
                      100
                    )}%`,

                    backgroundColor:
                      getSeverityColor(),
                  },
                ]}
              />

            </View>


            {/* GET ANALYSIS BUTTON */}
            <TouchableOpacity
              style={styles.analysisButton}
              onPress={() =>
                setShowAnalysis(!showAnalysis)
              }
              activeOpacity={0.7}
            >

              <View style={styles.analysisButtonLeft}>

                <MaterialCommunityIcons
                  name="chart-box-outline"
                  size={21}
                  color={COLORS.primary}
                />

                <Text style={styles.analysisButtonText}>
                  {showAnalysis
                    ? "Hide Severity Analysis"
                    : "Get Severity Analysis"}
                </Text>

              </View>

              <MaterialCommunityIcons
                name={
                  showAnalysis
                    ? "chevron-up"
                    : "chevron-down"
                }
                size={24}
                color={COLORS.primary}
              />

            </TouchableOpacity>


            {/* EXPANDED MULTI-FACTOR ANALYSIS */}
            {showAnalysis && (

              <View style={styles.analysisContainer}>

                <View style={styles.analysisHeader}>

                  <MaterialCommunityIcons
                    name="chart-areaspline"
                    size={22}
                    color={COLORS.primary}
                  />

                  <Text style={styles.analysisTitle}>
                    Multi-Factor Analysis
                  </Text>

                </View>


                {/* LESION AREA */}
                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Lesion Area
                  </Text>

                  <Text style={styles.factorValue}>
                    {lesionArea || "0"}%
                  </Text>

                </View>


                {/* LESION COUNT */}
                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Lesion Count
                  </Text>

                  <Text style={styles.factorValue}>
                    {lesionCount || "0"}
                  </Text>

                </View>


                {/* AVG LESION SIZE */}
                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Average Lesion Size
                  </Text>

                  <Text style={styles.factorValue}>
                    {avgLesionSize || "0"} px
                  </Text>

                </View>


                {/* COLOR SCORE */}
                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Colour Severity
                  </Text>

                  <Text style={styles.factorValue}>
                    {colorScore || "0"}%
                  </Text>

                </View>


                {/* DISTRIBUTION SCORE */}
                <View
                  style={[
                    styles.factorRow,
                    styles.lastFactorRow,
                  ]}
                >

                  <Text style={styles.factorLabel}>
                    Distribution Score
                  </Text>

                  <Text style={styles.factorValue}>
                    {distributionScore || "0"}%
                  </Text>

                </View>


                {/* INFO */}
                <View style={styles.infoBox}>

                  <MaterialCommunityIcons
                    name="information-outline"
                    size={18}
                    color={COLORS.gray}
                  />

                  <Text style={styles.infoText}>
                    Severity is estimated using multiple
                    lesion characteristics including affected
                    area, lesion count, colour and spatial
                    distribution.
                  </Text>

                </View>

              </View>

            )}

          </View>

        )}


        {/* ANALYZE ANOTHER LEAF */}
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/")}
        >

          <Text style={styles.buttonText}>
            Analyze Another Leaf
          </Text>

        </TouchableOpacity>

      </ScrollView>

    </SafeAreaView>
  );
}


const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },

  scrollContent: {
    padding: 20,
    paddingBottom: 30,
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


  // ============================
  // SEVERITY ANALYSIS BUTTON
  // ============================

  analysisButton: {
    marginTop: 20,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: "#EEEEEE",

    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  analysisButtonLeft: {
    flexDirection: "row",
    alignItems: "center",
  },

  analysisButtonText: {
    marginLeft: 8,
    fontSize: 16,
    fontWeight: "700",
    color: COLORS.primary,
  },


  // ============================
  // MULTI-FACTOR ANALYSIS
  // ============================

  analysisContainer: {
    marginTop: 16,
    backgroundColor: "#F8FAF8",
    borderRadius: 14,
    padding: 15,
  },

  analysisHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },

  analysisTitle: {
    marginLeft: 8,
    fontSize: 17,
    fontWeight: "700",
    color: COLORS.primary,
  },

  factorRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",

    paddingVertical: 12,

    borderBottomWidth: 1,
    borderBottomColor: "#E5E5E5",
  },

  lastFactorRow: {
    borderBottomWidth: 0,
  },

  factorLabel: {
    fontSize: 15,
    color: COLORS.gray,
    fontWeight: "500",
  },

  factorValue: {
    fontSize: 16,
    color: COLORS.primary,
    fontWeight: "700",
  },


  // ============================
  // INFORMATION BOX
  // ============================

  infoBox: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: "#E5E5E5",

    flexDirection: "row",
    alignItems: "flex-start",
  },

  infoText: {
    flex: 1,
    marginLeft: 7,
    fontSize: 12,
    lineHeight: 18,
    color: COLORS.gray,
  },


  // ============================
  // MAIN BUTTON
  // ============================

  button: {
    marginTop: 25,
    backgroundColor: COLORS.primary,
    paddingVertical: 18,
    borderRadius: 18,
    alignItems: "center",
  },

  buttonText: {
    color: "white",
    fontWeight: "700",
    fontSize: 18,
  },

});