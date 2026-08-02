import React from "react";
import {
  Modal,
  View,
  Text,
  ActivityIndicator,
  StyleSheet,
} from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { COLORS } from "../constants/colors";

interface LoadingOverlayProps {
  visible: boolean;
}

export default function LoadingOverlay({
  visible,
}: LoadingOverlayProps) {
  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
    >
      <View style={styles.overlay}>
        <View style={styles.card}>

          <MaterialCommunityIcons
            name="leaf"
            size={60}
            color={COLORS.primary}
          />

          <Text style={styles.title}>
            Analyzing Leaf...
          </Text>

          <Text style={styles.subtitle}>
            Our AI is analyzing your potato leaf.
            {"\n"}
            Please wait a moment.
          </Text>

          <ActivityIndicator
            size="large"
            color={COLORS.primary}
            style={{ marginTop: 20 }}
          />

        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.45)",
    justifyContent: "center",
    alignItems: "center",
  },

  card: {
    width: "85%",
    backgroundColor: "white",
    borderRadius: 22,
    padding: 30,
    alignItems: "center",
    elevation: 8,
  },

  title: {
    marginTop: 15,
    fontSize: 24,
    fontWeight: "700",
    color: COLORS.primary,
  },

  subtitle: {
    marginTop: 12,
    fontSize: 15,
    textAlign: "center",
    color: COLORS.gray,
    lineHeight: 22,
  },
});