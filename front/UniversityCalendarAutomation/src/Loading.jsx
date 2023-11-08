import styles from "./Loading.module.css";

export default function Loading() {
  return (
    <div className = { styles.spinnerContainer }>
      <div className = { styles.spinner }>
      </div>
    </div>
  );
}
