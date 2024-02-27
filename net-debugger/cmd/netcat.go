package cmd

import (
	"github.com/feliux/sec-tools/net-debbuger/netcat"
	"github.com/spf13/cobra"
)

// netcatCmd represents the netcat command
var netcatCmd = &cobra.Command{
	Use:   "netcat",
	Short: "Minimal netcat tool",
	Long: `
Connect to somewhere:  nc -a [hostname] -p [port]
Listen for inbound:    nc -l -a [hostname] -p [port]
	`,
	Run: func(cmd *cobra.Command, args []string) {
		listen, _ := cmd.Flags().GetBool("listen")
		addr, _ := cmd.Flags().GetString("address")
		port, _ := cmd.Flags().GetInt("port")
		zero, _ := cmd.Flags().GetBool("zero")
		if listen {
			netcat.StartServer(addr, port)
		} else {
			netcat.StartClient(addr, port, zero)
		}
	},
}

func init() {
	rootCmd.AddCommand(netcatCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// netcatCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	netcatCmd.Flags().BoolP("listen", "l", false, "listen mode, for inbound connects.")
	netcatCmd.Flags().StringP("address", "a", "localhost", "hostname to connect (client).")
	netcatCmd.Flags().IntP("port", "p", 5000, "port to connect (client) or bind (server).")
	netcatCmd.Flags().BoolP("zero", "z", false, " zero-I/O mode (used for scanning)")
}
