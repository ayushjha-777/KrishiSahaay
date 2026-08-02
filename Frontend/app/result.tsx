import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Alert,
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

  // AI Recommendation states
  const [recommendation, setRecommendation] = useState("");
  const [loadingRecommendation, setLoadingRecommendation] =
    useState(false);

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

  // =====================================================
  // GEMINI AI RECOMMENDATION
  // =====================================================

  const generateRecommendation = async () => {
    try {
      setLoadingRecommendation(true);

      const response = await fetch(
        "http://127.0.0.1:8000/api/recommend/",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            disease: diseaseName,

            confidence: Number(confidence),

            severity_level: hasSeverity
              ? String(severityLevel)
              : "Healthy",

            severity_percent: hasSeverity
              ? Number(severityPercent)
              : 0,

            lesion_area: hasSeverity
              ? Number(lesionArea)
              : 0,

            lesion_count: hasSeverity
              ? Number(lesionCount)
              : 0,

            avg_lesion_size: hasSeverity
              ? Number(avgLesionSize)
              : 0,

            color_score: hasSeverity
              ? Number(colorScore)
              : 0,

            distribution_score: hasSeverity
              ? Number(distributionScore)
              : 0,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.error ||
            "Unable to generate recommendation."
        );
      }

      if (!data.recommendation) {
        throw new Error(
          "No recommendation was returned."
        );
      }

      setRecommendation(data.recommendation);

    } catch (error) {
      console.error(
        "Recommendation error:",
        error
      );

      Alert.alert(
        "Recommendation Error",
        "Unable to generate AI recommendation. Please try again."
      );

    } finally {
      setLoadingRecommendation(false);
    }
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
                  {
                    color:
                      getSeverityColor(),
                  },
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
                      Math.max(
                        Number(severityPercent) || 0,
                        0
                      ),
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


            {/* EXPANDED ANALYSIS */}

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


                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Lesion Area
                  </Text>

                  <Text style={styles.factorValue}>
                    {lesionArea || "0"}%
                  </Text>

                </View>


                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Lesion Count
                  </Text>

                  <Text style={styles.factorValue}>
                    {lesionCount || "0"}
                  </Text>

                </View>


                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Average Lesion Size
                  </Text>

                  <Text style={styles.factorValue}>
                    {avgLesionSize || "0"} px
                  </Text>

                </View>


                <View style={styles.factorRow}>

                  <Text style={styles.factorLabel}>
                    Colour Severity
                  </Text>

                  <Text style={styles.factorValue}>
                    {colorScore || "0"}%
                  </Text>

                </View>


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


        {/* ============================================= */}
        {/* AI RECOMMENDATION */}
        {/* ============================================= */}

        <View style={styles.recommendationCard}>

          <View style={styles.recommendationHeader}>

            <View style={styles.aiIconContainer}>

              <MaterialCommunityIcons
                name="creation"
                size={24}
                color={COLORS.primary}
              />

            </View>

            <View style={styles.recommendationHeaderText}>

              <Text style={styles.recommendationTitle}>
                CropCare Insights
              </Text>

              <Text style={styles.aiPoweredText}>
                Know what your crop needs next
              </Text>

            </View>

          </View>


          {!recommendation && !loadingRecommendation && (

            <>

              <Text style={styles.recommendationDescription}>
                Get personalized crop-care guidance based on
                the detected disease, severity and lesion
                characteristics.
              </Text>

              <TouchableOpacity
                style={styles.generateButton}
                onPress={generateRecommendation}
                activeOpacity={0.8}
              >

                <MaterialCommunityIcons
                  name="creation"
                  size={20}
                  color="white"
                />

                <Text style={styles.generateButtonText}>
                  Get Care Plan
                </Text>

              </TouchableOpacity>

            </>

          )}


          {/* LOADING */}

          {loadingRecommendation && (

            <View style={styles.loadingContainer}>

              <ActivityIndicator
                size="large"
                color={COLORS.primary}
              />

              <Text style={styles.loadingText}>
                Analyzing crop condition...
              </Text>

              <Text style={styles.loadingSubText}>
                Generating personalized guidance
              </Text>

            </View>

          )}


          {/* GENERATED RECOMMENDATION */}

          {recommendation &&
            !loadingRecommendation && (

            <>

              <View style={styles.recommendationResult}>

                <Text style={styles.recommendationText}>
                  {recommendation}
                </Text>

              </View>


              {/* REGENERATE */}

              <TouchableOpacity
                style={styles.regenerateButton}
                onPress={generateRecommendation}
              >

                <MaterialCommunityIcons
                  name="refresh"
                  size={18}
                  color={COLORS.primary}
                />

                <Text style={styles.regenerateText}>
                  Generate New Recommendation
                </Text>

              </TouchableOpacity>

            </>

          )}

        </View>


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


  // ==========================================
  // SEVERITY ANALYSIS
  // ==========================================

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


  // ==========================================
  // AI RECOMMENDATION
  // ==========================================

  recommendationCard: {
    marginTop: 20,
    backgroundColor: COLORS.white,
    borderRadius: 20,
    padding: 20,
    elevation: 5,
  },

  recommendationHeader: {
    flexDirection: "row",
    alignItems: "center",
  },

  aiIconContainer: {
    width: 45,
    height: 45,
    borderRadius: 23,
    backgroundColor: "#EEF7EE",
    alignItems: "center",
    justifyContent: "center",
  },

  recommendationHeaderText: {
    marginLeft: 12,
    flex: 1,
  },

  recommendationTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: COLORS.primary,
  },

  aiPoweredText: {
    marginTop: 2,
    fontSize: 12,
    color: COLORS.gray,
  },

  recommendationDescription: {
    marginTop: 16,
    fontSize: 14,
    lineHeight: 21,
    color: COLORS.gray,
  },

  generateButton: {
    marginTop: 18,
    backgroundColor: COLORS.primary,
    paddingVertical: 14,
    borderRadius: 14,

    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },

  generateButtonText: {
    marginLeft: 8,
    color: "white",
    fontWeight: "700",
    fontSize: 15,
  },

  loadingContainer: {
    paddingVertical: 30,
    alignItems: "center",
  },

  loadingText: {
    marginTop: 14,
    fontSize: 15,
    fontWeight: "700",
    color: COLORS.primary,
  },

  loadingSubText: {
    marginTop: 4,
    fontSize: 12,
    color: COLORS.gray,
  },

  recommendationResult: {
    marginTop: 18,
    backgroundColor: "#F8FAF8",
    borderRadius: 14,
    padding: 16,
  },

  recommendationText: {
    fontSize: 14,
    lineHeight: 22,
    color: "#444444",
  },

  regenerateButton: {
    marginTop: 15,
    paddingVertical: 10,

    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
  },

  regenerateText: {
    marginLeft: 6,
    fontSize: 14,
    fontWeight: "600",
    color: COLORS.primary,
  },


  // ==========================================
  // MAIN BUTTON
  // ==========================================

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