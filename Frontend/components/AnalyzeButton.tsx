import React from "react";
import {
  TouchableOpacity,
  Text,
  ActivityIndicator,
  StyleSheet,
} from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../constants/colors";

interface AnalyzeButtonProps {
  onPress: () => void;
  loading: boolean;
}

export default function AnalyzeButton({
  onPress,
  loading,
}: AnalyzeButtonProps) {
  return (
    <TouchableOpacity
      style={styles.button}
      onPress={onPress}
      disabled={loading}
      activeOpacity={0.8}
    >
      {loading ? (
        <ActivityIndicator color="white" />
      ) : (
        <>
          <MaterialCommunityIcons
            name="leaf"
            size={22}
            color="white"
          />

          <Text style={styles.text}>
            Analyze Image
          </Text>
        </>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    marginTop: 30,
    marginHorizontal: 20,
    backgroundColor: COLORS.primary,
    borderRadius: 18,
    paddingVertical: 18,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    elevation: 5,
  },

  text: {
    color: "white",
    fontSize: 18,
    fontWeight: "700",
    marginLeft: 10,
  },
});