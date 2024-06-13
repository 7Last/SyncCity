package com.sevenlast.synccity.utils;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigLoader {
    private final Properties properties = new Properties();

    public ConfigLoader(String env) {
        loadProperties(env);
    }

    private void loadProperties(String env) {
        String propertiesFile = env + ".properties";
        try (InputStream input = new FileInputStream(propertiesFile)) {
            properties.load(input);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    public String getProperty(String key) {
        return properties.getProperty(key);
    }
}