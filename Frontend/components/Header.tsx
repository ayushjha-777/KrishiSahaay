import { View, Text, StyleSheet } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import { COLORS } from "../constants/colors";

export default function Header() {
  return (
    <LinearGradient
      colors={["#E8F5E9", "#F5FFF4"]}
      style={styles.container}
    >
      <View style={styles.logoContainer}>
        <MaterialCommunityIcons
          name="leaf"
          size={60}
          color={COLORS.primary}
        />
      </View>

      <Text style={styles.title}>KrishiSahaay</Text>

      <Text style={styles.subtitle}>
        AI Powered Disease Detection
      </Text>

      <Text style={styles.description}>
        Detect potato leaf diseases instantly using Artificial Intelligence
      </Text>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    paddingTop: 60,
    paddingBottom: 35,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },

  logoContainer: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: "#DDF5DF",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 15,
  },

  title: {
    fontSize: 36,
    fontWeight: "700",
    color: COLORS.primary,
  },

  subtitle: {
    fontSize: 18,
    marginTop: 5,
    fontWeight: "600",
    color: COLORS.text,
  },

  description: {
    marginTop: 12,
    textAlign: "center",
    width: "82%",
    color: COLORS.gray,
    fontSize: 15,
    lineHeight: 22,
  },
});